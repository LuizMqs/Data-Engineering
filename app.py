from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from analysis.suicides_by_year import df_merge_pop_total_suicides_total
from analysis.suicides_by_gender import df_number_of_suicides_by_gender, df_variation_of_suicides_by_gender_between_2010_and_2019
from analysis.suicides_by_race import df_number_of_suicides_by_race, df_number_of_suicides_by_race_between_2016_and_2019

df_total_suicides_total = df_merge_pop_total_suicides_total
df_variation_of_suicides_by_gender = df_variation_of_suicides_by_gender_between_2010_and_2019
df_number_of_suicides_by_race_between = df_number_of_suicides_by_race_between_2016_and_2019

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
                {'label': 'Ano', 'value': 'ano'},
                {'label': 'Gênero', 'value': 'genero'},
                {'label': 'Raça', 'value': 'raca'},
                {'label': 'Macrorregião', 'value': 'macrorregiao'},
            ],
            value='ano',
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
    if selected_value == 'ano':
        fig_line = px.line(
            df_total_suicides_total,
            x='year',
            y='suicide_rate',
            title='Taxa de Suicídio por Ano (2010 - 2019) ',
            labels={'year': 'Ano', 'suicide_rate': 'Taxa de Suicídio (100.000 habitantes)'}
        )
        
        figures = dcc.Graph(figure=fig_line)
        
    elif selected_value == 'genero':
        fig_line = px.pie(
            df_number_of_suicides_by_gender,
            values='amount_of_ suicides',
            names='gender',
            title='Taxa de suicídio por gênero'
        )
        
        fig_scatter = go.Figure()
        
        fig_scatter.add_trace(go.Scatter(
            x=df_variation_of_suicides_by_gender['year'],
            y=df_variation_of_suicides_by_gender['Variation_Male'],
            name="Masculino"
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_variation_of_suicides_by_gender['year'],
            y=df_variation_of_suicides_by_gender['Variation_Female'],
            name="Feminino"
        ))
        
        fig_scatter.update_layout(title="Taxa de dispersao entre os generos", xaxis_title="Anos", yaxis_title="Dispersao", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.35})
        
        figures = [
            dcc.Graph(figure=fig_scatter),
            dcc.Graph(figure=fig_line)
        ]

    elif selected_value == 'raca':
        
        fig_pie = px.pie(
            df_number_of_suicides_by_race,
            values='amount_of_ suicides',
            names='race',
            title='Taxa de suicídio por gênero'
        )
        
        fig_scatter = go.Figure()
        
        fig_scatter.add_trace(go.Scatter(
            x=df_number_of_suicides_by_race_between['year'],
            y=df_number_of_suicides_by_race_between['Amarela'],
            name='Amarela'
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_number_of_suicides_by_race_between['year'],
            y=df_number_of_suicides_by_race_between['Branca'],
            name='Branca'
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_number_of_suicides_by_race_between['year'],
            y=df_number_of_suicides_by_race_between['Parda'],
            name='Parda'
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_number_of_suicides_by_race_between['year'],
            y=df_number_of_suicides_by_race_between['Indígena'],
            name='Indígena'
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_number_of_suicides_by_race_between['year'],
            y=df_number_of_suicides_by_race_between['Preta'],
            name='Preta'
        ))
        
        fig_scatter.update_layout(title="Taxa de dispersao entre os generos", xaxis_title="Anos", yaxis_title="Dispersao", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.35})
        
        figures = [
            dcc.Graph(figure=fig_scatter),
            dcc.Graph(figure=fig_pie)
        ]
        
    #elif selected_value == 'macrorregiao':
        
        #figures = figure=fig_scatter
        
    else: 
        figures = dcc.Graph(
            figure = px.bar(
                df_variation_of_suicides_by_gender,
                values=['Feminino', 'Masculino'],
                names=['Feminino', 'Masculino'],
                title='Distribuição da Taxa de Suicídio por Gênero'
            )
        )
    return figures

#Executando o aplicativo
if __name__ == '__main__':
    app.run_server(debug=True)