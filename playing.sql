with
p as (select p.* from 'data/players.json' p),
t as (select unnest(t.success.teams, max_depth := 2) from 'data/teams.json' t),
l as (select id, name, unnest(flatten([t.lineup.DEF, t.lineup.MID, t.lineup.FWD, t.lineup.RUC, t.lineup.FLX, t.bench, t.injuryReplacement])) as lineup from t),
rfa as (select unnest(rfa.success.players, max_depth := 2) from 'data/free-agents.json' rfa),
i as (select i.* from 'data/injuries.json' i)

select p.id, p.firstName, p.lastName, rfa.restrictedTo, p.stats.averagePoints, i.eta, i.updated from p
left join rfa on p.id = rfa.playerId
left join l on p.id = l.lineup
left join i on i.name = concat(p.firstName, ' ', p.lastName) 
where p.status = 'playing' and
l.id is null
order by p.stats.averagePoints asc;