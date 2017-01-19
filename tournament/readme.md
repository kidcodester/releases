**BACKGROUND**  

The collection of files in this repository together form a small project to  
to demonstrate the use of a PostgreSQL database backend supporting a Python
application which aims to test and recreate a Swiss pairings (Swiss-System)
style tournament.

A Swiss-System tournament is one which in no players are eliminated but
for which players with similar scores are grouped together in progressive
tournament stages until a ranking of players is rendered.  Relative rankings
among players are thus revealed via accumulated scores at the end of the 
tournament with the winner ranking highest in terms of accumlated score.


**REQUIREMENTS**  

The project files are Python and PostgreSQL scripts, thus both Python  
and PostgreSQL are required to run this application.  In addition,  
the psycopg2 DB-API (Database-Application Programming Interface) is  
used to facilitate application-database communication.  

The project was written for Linux-style command-line invocation and  
was specifically built and tested in GitBash using a development environment  
set up by Vagrant running Oracle VirtualBox and PostgreSQL.  

For more information and to download/install these applications, please see:  

1). GitBash:  
https://git-for-windows.github.io/  

2). VirtualBox:  
https://www.virtualbox.org/wiki/Downloads  

3). Vagrant:  
https://www.vagrantup.com/  


**INSTALLATION**  

Please fork this project and then clone it to your local computer.  

When launching/running the application and/or associated components, be sure  
to know the local directory location where the project has been saved so that  
you may change directories in a terminal session to point to the application  
files.  


**FILE DESCRIPTION**  

The project consists of 3 files, described below.  

1). tournament.sql

This file creates (and/or recreates) the PostgreSQL database and associated  
objects required for the application.  Specifically, it creates:  
   a). the tournament database  
   b). two tables - players and matches  
   c). three views - vw_standings, vw_matchprep, and vw_pairings  

This file may be invoked on the command line in PostgreSQL (psql) session  
using the following command:  

\i [pathTo]/tournament.sql

Run this command first to set up the database.  Assuming the aforementioned  
prerequisite components have been correctly installed and set-up or a similar  
development environment is in use, the database should set up correctly.  

Upon running, run the \d command to see a list of database objects.  

2). tournament.py  

This is the main application file which carries out dedicated tasks in the  
tournament database.  Through the psycopg2 module, it has functions  
responsible for adding/deleting players and match results to the database  
as well as for returning standings and pairings.  

3). tournament_test.py  

This is the tester application which calls tournament.py by importing all
components in the specified tournament directory.  In so doing, the tester
progresses through a 10-step testing and verification process which includes
the following (with reference to function names in tournament.py):  

    1. countPlayers() returns 0 after initial deletePlayers() execution.  
    2. countPlayers() returns 1 after one player is registered.  
    3. countPlayers() returns 2 after two players are registered.  
    4. countPlayers() returns zero after registered players are deleted.  
    5. Player records successfully deleted.  
    6. Newly registered players appear in the standings with no matches.  
    7. After a match, players have updated standings.  
    8. After match deletion, player standings are properly reset.  
    9. Matches are properly deleted.  
    10. After one match, players with one win are properly paired.  


If all tests pass successfully, the following message should appear at the end:  
Success!  All tests pass!  

This file may likewise be invoked from the command line the aformentioned  
environment (or similar setup) with access to the initialized PostgreSQL  
database:  

python [pathTo]/tournament_test.py

Enjoy the demonstration!