CREATE TABLE players (
	player_id serial primary_key,
	player_name text
);

CREATE TABLE matches (
	match_id integer,
	player_id integer references players,
	outcome text
);