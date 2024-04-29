import pyodbc
import pandas as pd

file = pyodbc.connect('Driver={SQL Server};'
'Server=localhost;'
'Database=MCC;'
'Trusted_Connection=yes;')

cursor = file.cursor()

cursor.execute('''SELECT NomeAluna, AnoIngresso, SerieIngresso, NomeEscola, AlunosMatriculados, Municipio, Estado, Habitantes, IDH, Latitude, Longitude, Email, Distancia 
                FROM Alunas A
                INNER JOIN Escolas E ON A.Id_Escola = E.Id_Escola
                INNER JOIN Municipios M ON E.Id_Municipio = M.Id_Municipio
                WHERE SerieIngresso IN ('1 ano', '2 ano', '3 ano', '4 ano', 'outro')''')

colunas = [column[0] for column in cursor.description]

dictSQL = []
for row in cursor.fetchall():
    dictSQL.append(dict(zip(colunas, row)))

dfAlunas = pd.DataFrame.from_dict(dictSQL)

file.close()