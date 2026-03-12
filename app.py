import marimo

__generated_with = "0.20.4"
app = marimo.App(width="full")


@app.cell
def _():
    import marimo as mo
    import duckdb
    import httpx
    import json
    import os
    import asyncio
    from pathlib import Path
    from playwright.async_api import async_playwright
    from dotenv import load_dotenv

    load_dotenv(Path(__file__).parent / ".env")
    return Path, async_playwright, asyncio, duckdb, httpx, json, mo, os


@app.cell
def _(mo, os):
    cookie_input = mo.ui.text(
        label="Cookie (X-SID)",
        kind="password",
        value=os.environ.get("COOKIE", ""),
    )
    league_input = mo.ui.text(
        label="League ID",
        value=os.environ.get("LEAGUE", "4465"),
    )
    refresh_button = mo.ui.run_button(label="Refresh Data")

    mo.vstack([
        mo.md("## Configuration"),
        mo.md("_Set `COOKIE` and `LEAGUE` in a `.env` file to persist values._"),
        mo.hstack([cookie_input, league_input]),
        refresh_button,
    ])
    return cookie_input, league_input, refresh_button


@app.cell
async def _(
    Path,
    async_playwright,
    asyncio,
    cookie_input,
    duckdb,
    httpx,
    json,
    league_input,
    mo,
    refresh_button,
):
    mo.stop(not refresh_button.value)

    async def fetch_api_data(cookie: str, league: str):
        """Fetch data from AFL Fantasy Draft API."""
        cookies = {"X-SID": cookie}

        async with httpx.AsyncClient() as client:
            players = await client.get(
                "https://fantasydraft.afl.com.au/json/draft/players.json",
                cookies=cookies
            )
            teams = await client.get(
                f"https://fantasydraft.afl.com.au/api/en/draft/league/teams/{league}",
                cookies=cookies
            )
            free_agents = await client.get(
                f"https://fantasydraft.afl.com.au/api/en/draft/free-agents/list/{league}",
                cookies=cookies
            )

        players_data = players.json()
        teams_data = teams.json()
        free_agents_data = free_agents.json()

        Path("data").mkdir(exist_ok=True)
        Path("data/players.json").write_text(players.text)
        Path("data/teams.json").write_text(teams.text)
        Path("data/free-agents.json").write_text(free_agents.text)

        players_count = len(players_data)
        teams_count = len(teams_data.get("success", {}).get("teams", []))
        free_agents_count = len(free_agents_data.get("success", {}).get("players", []))

        return players_count, teams_count, free_agents_count

    async def scrape_injuries():
        """Scrape AFL injury list."""
        url = "https://www.afl.com.au/matches/injury-list"

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(url, wait_until="domcontentloaded")
            await page.wait_for_timeout(50)

            data = await page.evaluate("""
                () => Array.from(document.querySelectorAll("tbody")).flatMap((tbody) => {
                    const updated = tbody?.querySelector("tr:last-child td")?.innerText.replace("Updated: ", "");
                    return Array.from(
                        tbody.querySelectorAll("tr:has(td:nth-child(3):last-child)")
                    ).map((tr) => {
                        const [name, injury, eta] = Array.from(tr.children).map(
                            (td) => td.innerText
                        );
                        return { name, eta, updated };
                    });
                })
            """)

            await browser.close()

        Path("data/injuries.json").write_text(json.dumps(data))
        return len(data)

    async def fetch_last_year_stats(player_ids, batch_size=20):
        """Fetch 2025 stats for all players concurrently in batches. Skips if data already exists."""
        stats_dir = Path("data/players/2025")
        stats_dir.mkdir(parents=True, exist_ok=True)

        # Skip if directory already has files
        existing_files = list(stats_dir.glob("*.json"))
        if existing_files:
            return len(existing_files)

        semaphore = asyncio.Semaphore(batch_size)
        fetched_count = 0

        async def fetch_player(client: httpx.AsyncClient, player_id: int):
            nonlocal fetched_count
            async with semaphore:
                resp = await client.get(
                    f"https://fantasy.afl.com.au/json/draft/players_game_stats/2025/{player_id}.json"
                )
                if resp.status_code == 200:
                    (stats_dir / f"{player_id}.json").write_text(resp.text)
                    fetched_count += 1

        async with httpx.AsyncClient() as client:
            await asyncio.gather(*[fetch_player(client, pid) for pid in player_ids])

        return fetched_count

    players_count, teams_count, free_agents_count = await fetch_api_data(cookie_input.value, league_input.value)
    injury_count = await scrape_injuries()

    # Fetch 2025 stats for all players
    players_data = json.loads(Path("data/players.json").read_text())
    player_ids = [p["id"] for p in players_data]
    last_year_stats_count = await fetch_last_year_stats(player_ids)

    Path("database").mkdir(exist_ok=True)
    con = duckdb.connect("database/database.duckdb")
    con.execute("""
        create or replace view players as
        with
        p as (select p.* from 'data/players.json' p),
        t as (select unnest(t.success.teams, max_depth := 2) from 'data/teams.json' t),
        l as (select id, name, unnest(flatten([t.lineup.DEF, t.lineup.MID, t.lineup.FWD, t.lineup.RUC, t.lineup.FLX, t.bench, t.injuryReplacement])) as lineup from t),
        rfa as (select unnest(rfa.success.players, max_depth := 2) from 'data/free-agents.json' rfa),
        i as (select i.* from 'data/injuries.json' i),
        last_year as (
            select
                cast(regexp_extract(filename, '(\d+)\.json$', 1) as integer) as player_id,
                avg(
                    kicks * 3 +
                    handballs * 2 +
                    marks * 3 +
                    tackles * 4 +
                    freesFor * 1 +
                    freesAgainst * -3 +
                    hitouts * 1 +
                    goals * 6 +
                    behinds * 1
                ) as avg_points
            from read_json('data/players/2025/*.json', filename=true, union_by_name=true)
            group by player_id
        )

        select
            p.id as id,
            p.firstName as firstName,
            p.lastName as lastName,
            p.stats.averagePoints as average,
            round(last_year.avg_points, 1) as lastYearAvg,
            p.status as playingStatus,
            l.id as ownerId,
            rfa.restrictedTo as rfaDate,
            i.eta as injuryEta,
            i.updated as injuryUpdated
        from p
        left join rfa on p.id = rfa.playerId
        left join l on p.id = l.lineup
        left join i on i.name = concat(p.firstName, ' ', p.lastName)
        left join last_year on p.id = last_year.player_id
    """)

    mo.md(f"**Data refreshed.** {players_count} players, {teams_count} teams, {free_agents_count} free agents, {injury_count} injuries, {last_year_stats_count} last year stats.")
    return (con,)


@app.cell
def _(mo):
    mo.md("""
    ## All Players
    """)
    return


@app.cell
def _(con, mo):
    players = con.execute("select * from players").df()
    mo.ui.table(players)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Playing (Available)
    """)
    return


@app.cell
def _(con, mo):
    playing = con.execute("""
        select *
        from players
        where playingStatus = 'playing' and
        ownerId is null
        order by average desc
    """).df()
    mo.ui.table(playing)
    return


@app.cell
def _(mo):
    mo.md("""
    ## Returning (Injured)
    """)
    return


@app.cell
def _(con, mo):
    returning = con.execute("""
        select * from players
        where injuryEta is not null and
        ownerId is null
        order by average desc
    """).df()
    mo.ui.table(returning)
    return


if __name__ == "__main__":
    app.run()
