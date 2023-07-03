from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv('suicidios_2010_a_2019_cleaned.csv', dtype={'OCUP': str}, low_memory=False)

app = Dash(__name__)

#layout da página
app.layout = html.Div(
    id="allContainer",
    children=[
        html.H1("Taxa de suicídios entre 2010 e 2019", className="title"),
        
        #Radio buttons
        dcc.RadioItems(
            id='btnRadio',
            options=[
                {'label': 'Por estado', 'value': 'estado'},
                {'label': 'Por genero', 'value': 'genero'},
                {'label': 'Por idade', 'value': 'idade'},
            ],
            value='estado',
            className='buttonsRadio',
            inputStyle={'visibility': 'hidden'},  #oculta o radio button
        ),
        
        html.Div(id='graph-container', className="dashboard")
    ]
)

@app.callback(
    Output('graph-container', 'children'),
    [Input('btnRadio', 'value')]
)
def updateGraph(selected_value):
    if selected_value == 'estado':
        figure = dcc.Graph(
                    figure = px.bar(
                        df.groupby('estado').size().reset_index(name='Quantidade de Mortes'),
                        x='estado', 
                        y='Quantidade de Mortes',
                        title='Quantidade de suicídios por estado',
                        text='Quantidade de Mortes'
                    )
                )
    elif selected_value == 'genero':
        figure = dcc.Graph(
                    figure=px.pie(df, 
                        names='RACACOR', 
                        title='Distribuição das raças na ocorrência de suicídio')
                )
    else:
        figure = dcc.Graph(
                    figure = px.bar(
                        df,
                        x=df.groupby('ano')['age'].mean().index,
                        y=df.groupby('ano')['age'].mean()
                    )
                )
    
    return figure


#Executando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)