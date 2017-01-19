#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2

dbname = "tournament"

'''
    Note: foriegn-key constraints require simultaneous truncation
    of all inter-dependent tables (columns with FOREIGN KEY: REFERENCES)

    TRUNCATE TABLE <tab1>, <tab2>, <tab3>;
    tableTrunc = "TRUNCATE TABLE players, pairings, matches;"

    same as:

    TRUNCATE TABLE <tab1> CASCADE;
    tableTrunc = "TRUNCATE TABLE players CASCADE;"

    where CASCADE automatically applies truncate to other tables with
    referenced with foreign-key constraints.

'''


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname="+dbname)


def deleteMatches():
    """Remove all the match records from the database."""
    tableTrunc = "TRUNCATE TABLE matches;"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(tableTrunc)
    conn.commit()
    conn.close()


def deletePlayers():
    """Remove all the player records from the database."""
    tableTrunc = "TRUNCATE TABLE players CASCADE;"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(tableTrunc)
    conn.commit()
    conn.close()


def countPlayers():
    """Returns the number of players currently registered."""
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT CAST(COUNT(*) AS int) FROM players;")
    conn.close
    cnt = cursor.fetchone()[0]
    return cnt


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    add_player = "INSERT INTO players (player_name) VALUES(%s);"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(add_player, (name,))
    conn.commit()
    conn.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place,
    or a player tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vw_standings;")
    results = cursor.fetchall()
    conn.close()
    return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    match_result = "INSERT INTO matches (winner_id, loser_id) VALUES(%s,%s);"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(match_result, (winner, loser,))
    conn.commit()
    conn.close()


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

    pairings_query = "SELECT * FROM vw_pairings;"
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(pairings_query)
    pairings = cursor.fetchall()
    conn.close()
    return pairings
