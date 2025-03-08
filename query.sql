with
p as (select p.* from 'data/players.json' p),
t as (select unnest(t.success.teams, max_depth := 2) from 'data/teams.json' t),
l as (select id, name, unnest(flatten([t.lineup.DEF, t.lineup.MID, t.lineup.FWD, t.lineup.RUC, t.lineup.FLX, t.bench, t.injuryReplacement])) as lineup from t),
rfa as (select unnest(rfa.success.players, max_depth := 2) from 'data/free-agents.json' rfa)

select p.id, p.firstName, p.lastName, rfa.restrictedTo, p.stats.averagePoints from p
left join rfa on p.id = rfa.playerId
left join l on p.id = l.lineup
where p.status = 'playing'
and l.id is null;