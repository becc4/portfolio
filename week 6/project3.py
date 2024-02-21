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
SELECT b.playerID, b.yearID, cast(b.H as real) / b.AB as 'batting average'
FROM batting b
WHERE b.AB >= 1
ORDER BY cast(b.H as real) / b.AB desc, b.playerID
LIMIT 5
'''
table2a = pd.read_sql_query(query2a,con)
print("\n2a\n", table2a)

query2b = '''
SELECT b.playerID, b.yearID, cast(b.H as real) / b.AB as 'batting average'
FROM batting b
WHERE b.AB >= 10
ORDER BY cast(b.H as real) / b.AB desc, b.playerID
LIMIT 5
'''
table2b = pd.read_sql_query(query2b,con)
print("\n2b\n", table2b)

query2c = '''
SELECT b.playerID, cast(SUM(b.H) as real) / SUM(b.AB) as 'batting average'
FROM batting b
GROUP BY b.playerID
HAVING SUM(b.AB) >= 100
ORDER BY cast(SUM(b.H) as real) / SUM(b.AB) desc, b.playerID
LIMIT 5
'''
table2c = pd.read_sql_query(query2c,con)
print("\n2c\n", table2c)

query2cc = '''
SELECT b.playerID, SUM(b.H), SUM(b.AB), 
    cast(SUM(b.H) as real) / SUM(b.AB) as 'batting average'
FROM batting b
WHERE b.playerID = 'cobbty01'
GROUP BY b.playerID
'''
table2cc = pd.read_sql_query(query2cc,con)
print("\n2cc\n", table2cc)

query3 = '''
SELECT t.franchID, t.name, SUM(t.W), SUM(t.L)
FROM teams t
WHERE t.franchID = 'SEA' or t.franchID = 'TOR'
GROUP BY t.name
ORDER BY t.yearID
'''
table3 = pd.read_sql_query(query3,con)

#table = pd.read_sql_query(dataframe_query,con)
dataframe2 = pd.DataFrame(pd.read_sql_query(query3, con))
print(dataframe2)