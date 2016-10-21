-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

CREATE TABLE players (
	player_id serial primary key,
	player_name text
);

CREATE TABLE matches (
	player_id integer references players,
	outcome text
);

CREATE VIEW standings as 
	(select p.player_id, 
		p.player_name, 
		count(case when m.outcome = 'win' then 1 else null end) as wins,
		count(case when m.player_id notnull then 1 else null end) as matches
		from 
			players p
			left outer join matches m 
			on p.player_id = m.player_id
		group by p.player_id);
