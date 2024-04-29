from datasetAlunas import dfAlunas
from datasetEventos import dfEventos
from datasetOficinas import dfOficinas
import pandas as pd
import calendar
import locale

locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

df_alunas_municipios = dfAlunas.groupby('Municipio')[['NomeAluna']].count()
df_alunas_municipios = dfAlunas.drop_duplicates(subset='Municipio')[['Municipio', 'Latitude', 'Longitude', 'Distancia', 'AnoIngresso']].merge(df_alunas_municipios, left_on='Municipio', right_index=True).sort_values('NomeAluna', ascending=False)
df_alunas_municipios.columns = ['Municipio','latitude','longitude','Distancia', 'Ano','Alunas']

df_info_municipios = dfAlunas.drop_duplicates(subset='Municipio')[['Municipio', 'Habitantes', 'IDH']]

df_contato_alunas = dfAlunas[['NomeEscola', 'NomeAluna', 'AnoIngresso', 'Email']]

df_alunas_escolas = dfAlunas.groupby('NomeEscola')[['NomeAluna']].count()
df_alunas_escolas = dfAlunas.drop_duplicates(subset='NomeEscola')[['NomeEscola', 'Municipio', 'AlunosMatriculados', 'AnoIngresso']].merge(df_alunas_escolas, left_on='NomeEscola', right_index=True).sort_values('NomeAluna', ascending=False)
df_alunas_escolas.columns = ['Escola','Municipio','AlunosMatriculados', 'Ano', 'AlunasMCC']

df_alunas_serie = dfAlunas.groupby('SerieIngresso')[['NomeAluna']].count()
df_alunas_serie = dfAlunas.drop_duplicates(subset='SerieIngresso')[['SerieIngresso', 'AnoIngresso']].merge(df_alunas_serie, left_on='SerieIngresso', right_index=True).sort_values('NomeAluna', ascending=False)
df_alunas_serie.columns = ['Serie', 'Ano', 'Alunas']

df_eventos_locais = dfEventos.groupby('LocalExecucao')[['TituloEvento']].count()
df_eventos_locais = dfEventos.drop_duplicates(subset='LocalExecucao')[['LocalExecucao', 'Ano']].merge(df_eventos_locais, left_on='LocalExecucao', right_index=True).sort_values('TituloEvento', ascending=False)
df_eventos_locais.columns = ['Local', 'Ano', 'Eventos']

df_oficinas_youtube = dfOficinas[dfOficinas['OficinaYoutube'] != 0]

df_oficinas_sincronas = dfOficinas[dfOficinas['OficinaYoutube'] != 1]

df_alunas_oficinas = df_oficinas_sincronas.groupby('TituloOficina')[['AlunasParticipantes']].sum()
df_alunas_oficinas = df_oficinas_sincronas.drop_duplicates(subset='TituloOficina')[['TituloOficina', 'Ano']].merge(df_alunas_oficinas, left_on='TituloOficina', right_index=True).sort_values('AlunasParticipantes', ascending=False)
df_alunas_oficinas.columns = ['Oficina', 'Ano', 'Alunas']

df_alunas_oficinas_youtube = df_oficinas_youtube.groupby('TituloOficina')[['Visualizaoes']].sum()
df_alunas_oficinas_youtube = df_oficinas_youtube.drop_duplicates(subset='TituloOficina')[['TituloOficina', 'Ano']].merge(df_alunas_oficinas_youtube, left_on='TituloOficina', right_index=True).sort_values('Visualizaoes', ascending=False)
df_alunas_oficinas_youtube.columns = ['Oficina', 'Ano', 'Visualizacoes']

dfEventos['DataEvento'] = pd.to_datetime(dfEventos['DataEvento'])
dfEventos['Mes'] = dfEventos['DataEvento'].dt.strftime('%B')
dfEventos = dfEventos.dropna()
df_eventos_mes = dfEventos.groupby('Mes').size().reset_index(name='Eventos')
df_eventos_mes = df_eventos_mes[df_eventos_mes['Mes'].notna()]
dfEventos['Ano'] = dfEventos['DataEvento'].dt.year.astype(str).str.zfill(4)
df_eventos_mes_ano = dfEventos.groupby(['Mes', 'Ano']).size().reset_index(name='Eventos')
df_eventos_mes = df_eventos_mes.merge(df_eventos_mes_ano, on='Mes', how='left')
df_eventos_mes.columns = ['Mes', 'Eventos', 'Ano', 'EventosAnoMes']

def time_to_hours(time_str):
    parts = [float(x) for x in time_str.split(':')]
    hours = parts[0] + parts[1] / 60 + parts[2] / 3600
    return hours

dfOficinas['DuracaoOficina'] = dfOficinas['DuracaoOficina'].apply(time_to_hours)
