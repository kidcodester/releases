-- 1). CREATE & CONNECT TO DATABASE:

DROP DATABASE IF EXISTS tournament
;

CREATE DATABASE tournament
;

\c tournament
;


-- 2). CREATE REQUIRED TABLES:


CREATE TABLE IF NOT EXISTS players
(
	player_id SERIAL PRIMARY KEY
  , player_name VARCHAR(40) NOT NULL
);


/* note: winner_id & loser_id are foreign keys in matches table */

CREATE TABLE IF NOT EXISTS matches
(
	match_id SERIAL PRIMARY KEY
  , winner_id INTEGER REFERENCES players (player_id) NOT NULL
  , loser_id INTEGER REFERENCES players (player_id) NOT NULL
);


-- 3). CREATE REQUIRED VIEWS (all view objects prefixed: 'vw_')


/*

vw_standings: returns id-name-wins-total matches sorted by wins
Likely to be used frequently so we need a view for this.

*/

CREATE OR REPLACE VIEW vw_standings
AS
SELECT   wins.player_id AS player_id
	   , wins.player_name AS player_name
	   , wins.wins
       , total.matches
FROM
(
SELECT   ply.player_id
       , ply.player_name
       , COUNT(mat.winner_id) AS wins
FROM
		players		ply
LEFT OUTER JOIN
		matches		mat
	ON  ply.player_id = mat.winner_id
	GROUP BY ply.player_id, ply.player_name
) AS wins

JOIN

(
SELECT   ply.player_id
       , ply.player_name
       , COUNT(mat.match_id) AS matches
FROM
		players		ply
LEFT OUTER JOIN
		matches		mat
	ON  ply.player_id IN ( mat.winner_id, mat.loser_id)
	GROUP BY ply.player_id, ply.player_name
) AS total

ON   wins.player_id = total.player_id
;


/*

vw_matchprep: helper view which produces a unique row number
to each player-id to facilitate dividing players into two
groups for pairings.

Example: if 2 players had the same score, how would you
separate them? By using a unique row number we split into
odds and evens, at the very least.

*/

CREATE OR REPLACE VIEW vw_matchprep
AS
SELECT   row_number() OVER ( ORDER BY wins DESC)   AS rownum
       , *
FROM   vw_standings
ORDER BY wins DESC
; 

/*

vw_pairings - returns the actual swiss pairings by
performing a self-join to our helper vw_matchprep view.

Note all both of these last two views derive (directly or
indirectly) from the standings view which in turn reflects
any changes made in the matches table.

*/


CREATE OR REPLACE VIEW vw_pairings
AS
SELECT    set1.player_id   AS  id1
        , set1.player_name AS player1
        , set2.player_id   AS  id2
        , set2.player_name AS player2
FROM     vw_matchprep      set1
JOIN     vw_matchprep      set2
ON       MOD(set1.rownum,2) = 0
AND      MOD(set2.rownum,2) <> 0 
AND      set1.rownum = set2.rownum+1
;