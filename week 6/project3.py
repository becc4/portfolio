import pandas as pd 
import numpy as np
import sqlite3

# careful to list your path to the file or save it in the same place as your .qmd or .py file
sqlite_file = 'lahmansbaseballdb.sqlite'
con = sqlite3.connect(sqlite_file)

# You can see the list of tables available in the database
q = 'SELECT * FROM allstarfull LIMIT 5'
table = pd.read_sql_query(q,con)

# Write an SQL query to create a new dataframe about baseball players who attended BYU-Idaho
# PlayerID, SchoolID, Salary, YearID/TeamID for salary
dataframe_query = '''
SELECT cp.playerID, cp.schoolID, sal.salary, cp.yearID, sal.team_ID
FROM collegeplaying cp
INNER JOIN salaries sal
ON sal.playerID = cp.playerID
WHERE cp.schoolID = 'idbyuid'
ORDER BY sal.salary desc
'''
table = pd.read_sql_query(dataframe_query,con)

dataframe = pd.DataFrame(pd.read_sql_query(dataframe_query, con))
print(dataframe)

# Write an SQL query that provides playerID, yearID, and batting average for players with at least 1 at bat that year.
# batting average = hits / at-bats
"""
Key
AB - At Bat
H - Hits
"""
query2a = '''
SELECT b.playerID, b.yearID, (b.H / b.AB) as 'batting average'
FROM batting b
WHERE b.AB >= 1
GROUP BY b.playerID, b.yearID
ORDER BY b.playerID, b.yearID
'''
table2a = pd.read_sql_query(query2a,con)