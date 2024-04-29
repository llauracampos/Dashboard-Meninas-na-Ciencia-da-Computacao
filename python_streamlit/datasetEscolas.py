import pyodbc
import pandas as pd

file = pyodbc.connect('Driver={SQL Server};'
'Server=localhost;'
'Database=MCC;'
'Trusted_Connection=yes;')

cursor = file.cursor()

cursor.execute('''SELECT NomeEscola, AlunosMatriculados, Municipio, Estado, Nome, Telefone, Email 
                FROM Escolas E
                INNER JOIN Municipios M ON E.Id_Municipio = M.Id_Municipio
                INNER JOIN ResponsaveisEscolas RE ON E.Id_Responsavel = RE.Id_Responsavel''')

colunas = [column[0] for column in cursor.description]

dictSQL = []
for row in cursor.fetchall():
    dictSQL.append(dict(zip(colunas, row)))

dfEscolas = pd.DataFrame.from_dict(dictSQL)

file.close()