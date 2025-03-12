create or replace view players as
with
p as (select p.* from 'data/players.json' p),
t as (select unnest(t.success.teams, max_depth := 2) from 'data/teams.json' t),
l as (select id, name, unnest(flatten([t.lineup.DEF, t.lineup.MID, t.lineup.FWD, t.lineup.RUC, t.lineup.FLX, t.bench, t.injuryReplacement])) as lineup from t),
rfa as (select unnest(rfa.success.players, max_depth := 2) from 'data/free-agents.json' rfa),
i as (select i.* from 'data/injuries.json' i)

select 
    p.id as id, 
    p.firstName as firstName, 
    p.lastName as lastName,
    p.stats.averagePoints as average, 
    p.status as playingStatus,
    l.id as ownerId,
    rfa.restrictedTo as rfaDate, 
    i.eta as injuryEta, 
    i.updated as injuryUpdated 
from p
left join rfa on p.id = rfa.playerId
left join l on p.id = l.lineup
left join i on i.name = concat(p.firstName, ' ', p.lastName) 
