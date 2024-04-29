import pyodbc
import pandas as pd

file = pyodbc.connect('Driver={SQL Server};'
'Server=localhost;'
'Database=MCC;'
'Trusted_Connection=yes;')

cursor = file.cursor()

cursor.execute('''SELECT * FROM AnosExecucao''')

colunas = [column[0] for column in cursor.description]

dictSQL = []
for row in cursor.fetchall():
    dictSQL.append(dict(zip(colunas, row)))

dfAnos = pd.DataFrame.from_dict(dictSQL)

file.close()