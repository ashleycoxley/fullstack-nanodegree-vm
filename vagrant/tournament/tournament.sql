-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;
CREATE DATABASE tournament;
\c tournament


CREATE TABLE players (
	player_id serial primary key,
	player_name text
);


CREATE TABLE matches (
    match_id serial primary key,
    winner integer references players(player_id),
    loser integer references players(player_id)
);


CREATE VIEW player_wins as (
	select winner as player_id, count(*) as wins
		from matches
	group by winner
);

CREATE VIEW player_losses as (
	select loser as player_id, count(*) as losses
		from matches
	group by loser
);

CREATE VIEW standings as (
	select 
		p.player_id,
		p.player_name,
		case when (pw.wins is null) then 0 else pw.wins end as wins,
		case when (pw.wins is null and pl.losses is null) then 0 else coalesce(pw.wins + pl.losses, pw.wins, pl.losses) end matches
	from
		players p
		left outer join player_wins pw
		on p.player_id = pw.player_id
		left join player_losses pl
		on p.player_id = pl.player_id
	order by wins desc
);


