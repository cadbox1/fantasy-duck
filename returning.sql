select * from players
where injuryEta is not null and
ownerId is null
order by average asc;