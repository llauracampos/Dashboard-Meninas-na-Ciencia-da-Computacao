import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import folium
import plotly.graph_objs as go
from PIL import Image
from datasetEventos import dfEventos
from datasetAnos import dfAnos
from datasetAlunas import dfAlunas
from uteis import dfOficinas
from uteis import df_alunas_municipios
from uteis import df_info_municipios
from uteis import df_contato_alunas
from uteis import df_alunas_escolas
from uteis import df_alunas_serie
from uteis import df_eventos_mes
from uteis import df_eventos_locais
from uteis import df_oficinas_youtube
from uteis import df_alunas_oficinas
from uteis import df_alunas_oficinas_youtube
from streamlit_folium import st_folium
from streamlit_extras.metric_cards import style_metric_cards
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Meninas na Ciência da Computação",
    layout="wide")
st.title("Meninas na Ciência da Computação :computer:")



def pb_map (df):
    map = folium.Map(location=[-7, -32], zoom_start=8, scrollWheelZoom=True, tiles='CartoDB positron')
    
    choropleth = folium.Choropleth(
        geo_data='brazil-states.geojson',
        data=df_alunas_municipios,
        columns=('Municipio', 'Alunas'),
        key_on='feature.properties.name',
        fill_color='RdPu',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name'], labels=False)
    )

    st_map = st_folium(map, width=3000, height=550)

    city_name = ''
    if st_map['last_active_drawing']:
        city_name = st_map['last_active_drawing']['properties']['name']
    return city_name

def display_info (df, metric, info_name, title, column):
    if info_name:
        df = df[df[metric] == info_name]
        st.metric(title, df[column])


def display_list (df, metric, info_name, title):
    if info_name:
        df = df[df[metric] == info_name]
        
        st.write(title, df)

def display_header (df, metric, info_name, title, column):
    if info_name:
        df = df[df[metric] == info_name]

        text = df[metric]
        st.write(title, text)  

def display_year_sidebar(df):
    years = [''] + list(df['Ano'].unique())
    years.sort()

    return st.sidebar.selectbox('Ano', years)

def display_city_sidebar(df, city_name):
    cities = [''] + list(df['Municipio'].unique())
    cities.sort()
    index = cities.index(city_name) if city_name and city_name in cities else 0
    return st.sidebar.selectbox('Municipio', cities, index)

def display_school_sidebar(df, city_name):
    if city_name:
        df = df[df['Municipio'] == city_name]

        schools = [''] + list(df['Escola'].unique())
        schools.sort()
        index = schools.index(city_name) if city_name and city_name in schools else 0
        return st.sidebar.selectbox('Escola', schools, index)

def display_graf_alunas_escolas(df, school_name):
    if school_name:
        df = df[df['Escola'] == school_name]

        barra_total_alunos = go.Bar(
            x=df['Escola'],
            y=df['AlunosMatriculados'],
            name='Total de Alunos',
            marker_color='#DE8DAB'
        )

        barra_alunas_mcc = go.Bar(
            x=df['Escola'],
            y=df['AlunasMCC'],
            name='Alunas MCC',
            marker_color='#9C173D'
        )

        layout = go.Layout(
            title=dict(
                text='Relação entre Alunos Matriculados e Alunas do MCC',
                x=0.5,  
                y=0.95,   
                xanchor='center',
                yanchor='top'
            ),
            xaxis=dict(title='Escola'),
            yaxis=dict(title='Quantidade'),
            barmode='group' 
        )

        fig = go.Figure(data=[barra_total_alunos, barra_alunas_mcc], layout=layout)

        with st.container():
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('<style>div.stPlotlyChart {border: 1px solid rgba(155, 23, 60, 0.1) !important;}</style>', unsafe_allow_html=True)     

def display_graf_vertical(df, title, x, y):
    chart = px.bar(df, x=x, y=y, title=title, color_discrete_sequence=['#9B173C'])

    chart.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
    )

    with st.container():
        st.plotly_chart(chart, use_container_width=True)
        st.markdown('<style>div.stPlotlyChart {border: 1px solid rgba(155, 23, 60, 0.1) !important;}</style>', unsafe_allow_html=True)

def display_graf_horizontal(df, title, x, y):
    chart = px.bar(df, y=x, x=y, title=title, color_discrete_sequence=['#9B173C'])

    chart.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
    )

    with st.container():
        st.plotly_chart(chart, use_container_width=True)
        st.markdown('<style>div.stPlotlyChart {border: 1px solid rgba(155, 23, 60, 0.1) !important;}</style>', unsafe_allow_html=True)

def display_graf_donut(df, title, quantitative, nominal):
    chart = px.pie(df, values=quantitative, names=nominal, title=title)

    colors = ["#FFB3C2", "#9C173D", "#DB4675", "#A64B64", "#DE8DAB", "#DB9DA9", "#E0BFC8", "#992F58", "#A87E8B", "#731435"]

    chart.update_traces(marker=dict(colors=colors))

    chart.update_layout(
        title=dict(
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top',
            
        ),
        margin=dict(
            l=20,
            r=20,
            t=50,
            b=20
        ),
    )

    with st.container():
        st.plotly_chart(chart, use_container_width=True)
        st.markdown('<style>div.stPlotlyChart {border: 1px solid rgba(155, 23, 60, 0.1) !important;}</style>', unsafe_allow_html=True)

def somar_coluna(df, column):
    soma = df[column].sum()
    return soma

def contar_coluna(df, column):
    soma = df[column].count()
    return soma

aba1, aba2, aba3, aba4 = st.tabs(['Municipios', 'Alunas', 'Oficinas', 'Eventos'])
with aba1:
    years = display_year_sidebar(dfAnos)

    df_alunas_municipios = df_alunas_municipios[df_alunas_municipios['Ano'] == years]
    df_alunas_escolas = df_alunas_escolas[df_alunas_escolas['Ano'] == years]
    df_alunas_serie = df_alunas_serie[df_alunas_serie['Ano'] == years]
    df_contato_alunas = df_contato_alunas[df_contato_alunas['AnoIngresso'] == years]
    dfEventos = dfEventos[dfEventos['Ano'] == years]
    dfOficinas = dfOficinas[dfOficinas['Ano'] == years]
    df_eventos_locais = df_eventos_locais[df_eventos_locais['Ano'] == years]
    df_oficinas_youtube = df_oficinas_youtube[df_oficinas_youtube['Ano'] == years]  
    df_alunas_oficinas = df_alunas_oficinas[df_alunas_oficinas['Ano'] == years]
    df_alunas_oficinas_youtube = df_alunas_oficinas_youtube[df_alunas_oficinas_youtube['Ano'] == years]
    df_eventos_mes = df_eventos_mes[df_eventos_mes['Ano'] == years]

    city_name = pb_map(df_alunas_municipios)
    city_name = display_city_sidebar(df_alunas_municipios, city_name)
    school_name = display_school_sidebar(df_alunas_escolas, city_name)

    col1, col2 = st.columns(2)
    with col1:
        count = contar_coluna(df_alunas_municipios, 'Municipio')
        st.metric('Total de Municipios Visitados', df_alunas_municipios['Municipio'].count())
    with col2:
        sum = somar_coluna(df_alunas_municipios, 'Distancia')
        st.metric('Total de KM Percorridos', df_alunas_municipios['Distancia'].sum())

    if city_name:
        st.subheader(f'Informações do Município ({city_name})')

        col1, col2, col3 = st.columns(3)
        with col1:
            display_info(df_alunas_municipios, 'Municipio', city_name, 'Alunas atingidas', 'Alunas')
        with col2:
            display_info(df_info_municipios, 'Municipio', city_name, 'População', 'Habitantes')
        with col3:
            display_info(df_info_municipios, 'Municipio', city_name, 'IDH', 'IDH')

        if school_name:
            st.subheader(f'Informações da Escola ({school_name})')

            col1, col2 = st.columns(2)
            with col1:
                display_graf_alunas_escolas(df_alunas_escolas, school_name)
                
            with col2:
                display_list(df_contato_alunas, 'NomeEscola', school_name, 'Contato das Alunas')
    
with aba2:
    col1, col2 = st.columns(2)
    with col1:
        display_graf_vertical(df_alunas_municipios, 'Alunas por Municipio', 'Municipio', 'Alunas')    
    with col2:
        espaco_horizontal = Image.open('espacohorizontal.PNG')

        st.image(espaco_horizontal)

        st.write(f"<div style='text-align:center; font-weight:bold; font-size:16px'>Top 3: Escolas</div>", unsafe_allow_html=True)

        separador_horizontal = Image.open('separadorhorizontal.PNG')

        st.image(separador_horizontal)

        if years:
            dados = df_alunas_escolas.sort_values(by='AlunasMCC', ascending=False)

            top_3 = dados.head(3)

            gold_medal = Image.open('1.png')
            silver_medal = Image.open('2.png')
            bronze_medal = Image.open('3.png')
            espaco_vertical = Image.open('espacovertical.PNG')

            col1, col2, col3, col4, col5 = st.columns(5)

            with col1:
                st.image(espaco_vertical, width=10)
            with col2: 
                st.image(gold_medal, caption=top_3.iloc[0]['Escola'], width=150)
            with col3:
                st.image(silver_medal, caption=top_3.iloc[1]['Escola'], width=150)
            with col4:
                st.image(bronze_medal, caption=top_3.iloc[2]['Escola'], width=150)
            with col5:
                st.image(espaco_vertical, width=10)
        
    col1, col2 = st.columns(2)
    with col1:
        display_graf_donut(df_alunas_escolas, 'Alunas por Escola', 'AlunasMCC', 'Escola')
    with col2:
        display_graf_donut(df_alunas_serie, 'Alunas por Serie', 'Alunas', 'Serie')

with aba3:
    col1, col2, col3 = st.columns(3)
    with col1:
        count = contar_coluna(dfOficinas, 'TituloOficina')
        st.metric('Total de Oficinas', dfOficinas['TituloOficina'].count())
    with col2:
        sum = somar_coluna(dfOficinas, 'DuracaoOficina')
        total_horas = round(dfOficinas['DuracaoOficina'].sum(), 2)
        st.metric('Total de Horas/Aula', total_horas)
    with col3:
        sum = somar_coluna(df_oficinas_youtube, 'Visualizaoes')
        total_visualizacoes = int(sum)
        st.metric('Total de Visualizacoes (Youtube)', total_visualizacoes)    
    col1, col2 = st.columns(2)
    with col1:
        display_graf_horizontal(df_alunas_oficinas, 'Alunas por Oficina (Síncrona)', 'Oficina', 'Alunas')
    with col2:
        display_graf_horizontal(df_alunas_oficinas_youtube, 'Visualizacoes por Oficina (Youtube)', 'Oficina', 'Visualizacoes')

with aba4:

    col1, col2 = st.columns(2)
    with col1:
        display_graf_vertical(df_eventos_mes, 'Eventos por Mês', 'Mes', 'Eventos')
        display_graf_vertical(df_eventos_locais, 'Eventos por Local', 'Local', 'Eventos')
    with col2:
        display_graf_donut(dfEventos, 'Participantes por Evento', 'Participantes', 'TituloEvento')
        sum = somar_coluna(dfEventos, 'Participantes')
        st.metric('Total de Participantes', dfEventos['Participantes'].sum())
        count = contar_coluna(dfEventos, 'TituloEvento')
        st.metric('Total de Eventos', dfEventos['TituloEvento'].count())
        
    eventos = [''] + list(dfEventos['TituloEvento'].unique())
    eventos.sort()
    
    evento_selecionado = st.selectbox('TituloEvento', eventos)

    evento_filtrado = dfEventos[dfEventos['TituloEvento'] == evento_selecionado]

    if not evento_filtrado.empty:
        descricao = evento_filtrado.iloc[0]['DescricaoEvento']
        participantes = evento_filtrado.iloc[0]['Participantes']

        st.markdown("<h3><b>Descrição do Evento</b></h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:20px;'>{descricao}</p>", unsafe_allow_html=True)

        st.markdown("<h3><b>Participantes do Evento</b></h4>", unsafe_allow_html=True)
        st.markdown(f"<p style='font-size:20px;'>{participantes}</p>", unsafe_allow_html=True)
    else:
        st.write("Nenhum evento selecionado ou não encontrado.")

style_metric_cards(background_color="#FFE2EA",border_left_color="#A64B64",border_color="#EFC1D3",box_shadow="#EFC1D3")

   


