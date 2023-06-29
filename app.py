from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('suicidios_2010_a_2019_cleaned.csv', dtype={'OCUP': str}, low_memory=False)

app = Dash(__name__)

#layout da página
app.layout = html.Div(
    children=[
        html.H1("Taxa de suicídios entre 2010 e 2019", className="title"),
        
        #Quantidade de suicídios com o passar dos anos (Gráfico de linhas)
        html.Div(
            children=[
                dcc.Graph(
                    figure = px.line(
                        df.groupby('ano').size().reset_index(name='Quantidade de Mortes'),
                        x='ano', 
                        y='Quantidade de Mortes',
                        title='Quantidade de suicídios com o passar dos anos'
                    )
                ),
            ],
            className="dashboard"
        ),
        
        #Diferenças entre as quantidades de suicídios em relação à população nos estados brasileiros (Gráfico de barras):
        html.Div(
            children=[
                dcc.Graph(
                    figure = px.bar(
                        df.groupby('estado').size().reset_index(name='Quantidade de Mortes'),
                        x='estado', 
                        y='Quantidade de Mortes',
                        title='Quantidade de suicídios por estado',
                        text='Quantidade de Mortes'
                    )
                ),
            ],
            className="dashboard"
        ),
        
        #Existe alguma raça (classificação de acordo com o IBGE) que comete um maior número de suicídio? (Gráfico de pizza):
        html.Div(
            children=[
                dcc.Graph(
                    figure=px.pie(df, 
                        names='RACACOR', 
                        title='Distribuição das raças na ocorrência de suicídio')
                ),
            ],
            className="dashboard"
        ),
        
        #Existe algum gênero (classificação de acordo com o IBGE) que comete um maior número de suicídio? (Gráfico de pizza)
        html.Div(
            children=[
                dcc.Graph(
                    figure=px.pie(df, 
                        names='SEXO', 
                        title='Distribuição dos gêneros na ocorrência de suicídio')
                ),
            ],
            className="dashboard"
        ),
        
        #Existe algum gênero correlacionado a alguma raça que comete um maior número de suicídio? (Gráfico de barras empilhadas)
        html.Div(
            children=[
                dcc.Graph(
                    figure = px.bar(
                        df.groupby(['RACACOR', 'SEXO']).size().reset_index(),
                        x='SEXO', 
                        color='SEXO',
                        title='Distribuição das raças e gêneros na ocorrência de suicídio',
                        text=df.groupby(['RACACOR', 'SEXO']).size().reset_index().apply(lambda x: f"{x['RACACOR']} - {x[0]}", axis=1),
                        hover_name='RACACOR',
                        barmode='group'
                    )
                ),
            ],
            className="dashboard"
        ),
        
        #Correlação entre formas de suicídio e gênero? (Gráfico de barras)
        html.Div(
            children=[
                dcc.Graph(
                    figure = px.bar(
                        df.groupby(['CAUSABAS', 'SEXO']).size().reset_index(),
                        x='CAUSABAS',
                        y='SEXO', 
                        color='SEXO',
                        title='Correlação entre formas de suicídio e gênero',
                        barmode='group'
                        #Aguardar a correlação dos CIDs para realizar a correção
                    )
                ),
            ],
            className="dashboard"
        ),
        
        #Correlação entre formas de suicídio e raça? (Gráfico de barras)
        html.Div(
            children=[
                dcc.Graph(
                    figure = px.bar(
                        df.groupby(['CAUSABAS', 'RACACOR']).size().reset_index(),
                        x='CAUSABAS', 
                        y='RACACOR',
                        color='RACACOR',
                        title='Correlação entre formas de suicídio e raça',
                        barmode='group'
                        #Aguardar a correlação dos CIDs para realizar a correção
                    )
                ),
            ],
            className="dashboard"
        ),
        
        #Correlação entre formas de suicídio, raça e gênero (Gráfico de barras empilhadas)
        html.Div(
            children=[
                dcc.Graph(
                    figure = px.bar(
                        df.groupby(['CAUSABAS', 'RACACOR', 'SEXO']).size().reset_index(),
                        x='CAUSABAS', 
                        y=0,
                        color='RACACOR',
                        title='Correlação entre formas de suicídio, raça e gênero',
                        barmode='stack',
                        facet_col='SEXO'
                        #Aguardar a correlação dos CIDs para realizar a correção
                    )
                ),
            ],
            className="dashboard"
        ),
        
        #Correlação de idade e taxa de suicídio (Gráfico de dispersão)
        #falta dados
        
    ]
)

#Executando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)