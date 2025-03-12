select *
from players
where playingStatus = 'playing' and
ownerId is null
order by average asc;