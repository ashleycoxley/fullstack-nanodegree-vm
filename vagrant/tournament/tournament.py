#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


def execute_query(sql_statement, values=None):
    """Execute a sql statement and return the query result."""
    db = connect()
    cursor = db.cursor()
    if values:
        cursor.execute(sql_statement, values)
    else:
        cursor.execute(sql_statement)
    try:
        result = cursor.fetchall()
    except psycopg2.ProgrammingError:
        result = None
    db.commit()
    db.close()
    return result


def deleteMatches():
    """Remove all the match records from the database."""
    delete_matches_statement = 'delete from matches'
    execute_query(delete_matches_statement)


def deletePlayers():
    """Remove all the player records from the database."""
    delete_players_statement = "delete from players"
    execute_query(delete_players_statement)


def countPlayers():
    """Returns the number of players currently registered."""
    count_players_statement = "select count(*) from players"
    player_count_result = execute_query(count_players_statement)
    player_count = player_count_result[0][0]
    return player_count


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    register_player_statement = "insert into players (player_name) values (%s)"
    register_player_values = (name,)
    execute_query(register_player_statement, register_player_values)


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    standings_statement = "select * from standings order by wins desc;"
    standings_result = execute_query(standings_statement)
    return standings_result


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    winner_match_statement = """insert into matches (player_id, outcome)
        values (%s, 'win')"""
    winner_values = (winner,)
    loser_match_statement = """insert into matches (player_id, outcome)
        values (%s, 'loss')"""
    loser_values = (loser,)
    execute_query(winner_match_statement, winner_values)
    execute_query(loser_match_statement, loser_values)
 
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    current_standings = playerStandings()
    next_round = []
    match_count = 0
    for player_row in current_standings:
        player_id = player_row[0]
        name = player_row[1]
        if match_count == 0:
            match_list = [player_id, name]
            match_count += 1
        elif match_count == 1:
            match_list += [player_id, name]
            next_round.append(tuple(match_list))
            match_count = 0
    return next_round


