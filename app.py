from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from analysis.suicides_by_year import df_merge_pop_total_suicides_total
from analysis.suicides_by_gender import df_number_of_suicides_by_gender, df_variation_of_suicides_by_gender_between_2010_and_2019
from analysis.suicides_by_race import df_number_of_suicides_by_race, df_number_of_suicides_by_race_between_2016_and_2019
from analysis.suicides_by_cause_of_death import df_death_cause_description_and_amount
from analysis.suicides_and_idh import df_idh_and_suicide_rate
from analysis.suicides_by_macro_region_and_year import df_suicides_by_year_and_macro_regions_formated

df_total_suicides_total = df_merge_pop_total_suicides_total
df_variation_of_suicides_by_gender = df_variation_of_suicides_by_gender_between_2010_and_2019
df_number_of_suicides_by_race_between = df_number_of_suicides_by_race_between_2016_and_2019
df_death_cause_description = df_death_cause_description_and_amount

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
                {'label': 'Taxa', 'value': 'ano'},
                {'label': 'Gênero', 'value': 'genero'},
                {'label': 'Raça', 'value': 'raca'},
                {'label': 'Causas', 'value': 'causas'},
                {'label': 'IDH', 'value': 'idh'},
                {'label': 'Macrorregião', 'value': 'macrorregiao'} 
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
            y=df_variation_of_suicides_by_gender['Masculino'],
            name="Masculino"
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_variation_of_suicides_by_gender['year'],
            y=df_variation_of_suicides_by_gender['Feminino'],
            name="Feminino"
        ))
        
        fig_scatter.update_layout(title="Taxa de Suicídios entre os gêneros", xaxis_title="Anos", yaxis_title="Suicídios", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.35})
        
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
        
        fig_scatter.update_layout(title="Taxa de Suícidio por Raça", xaxis_title="Anos", yaxis_title="Suicídios", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.5})
        
        figures = [
            dcc.Graph(figure=fig_scatter),
            dcc.Graph(figure=fig_pie)
        ]
        
    elif selected_value =='idh': 
        
        fig_scatter = go.Figure()
        
        fig_scatter.add_trace(go.Scatter(
            x=df_idh_and_suicide_rate['year'],
            y=df_idh_and_suicide_rate['idh'],
            name='Índice de Desenvolvimento Humano'
        ))
        
        fig_scatter.add_trace(go.Scatter(
            x=df_idh_and_suicide_rate['year'],
            y=df_idh_and_suicide_rate['suicide_rate'],
            name='Taxa de suicídio'
        ))
        
        fig_scatter.update_layout(title="Índice de Desenvolvimento Humano - IDH", xaxis_title="Anos", yaxis_title="Suicídios", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.5})
        
        figures = dcc.Graph(figure=fig_scatter)
        
    elif selected_value == 'macrorregiao': #df_suicides_by_year_and_macro_regions_formated
        
        fig_scatter = px.line(
            df_suicides_by_year_and_macro_regions_formated,
            x='year',
            y='total_deaths',
            color='region',
            markers=True
        )        
        fig_scatter.update_layout(title="Número de Mortes por Região ao longo dos anos", xaxis_title="Anos", yaxis_title="Total de mortes", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.4})
        
        fig_scatter2 = px.line(
            df_suicides_by_year_and_macro_regions_formated,
            x='year',
            y='suicide_rate',
            color='region',
            markers=True
        )
        fig_scatter2.update_layout(title="Taxa de Suicídio por Região ao longo dos anos", xaxis_title="Anos", yaxis_title="Taxa de suicídios", legend_orientation='h', legend_valign="bottom",legend_title_text="Legenda", legend_title_side="top", legend = {"yanchor": "bottom", "y": -0.4})
        
        figures = [dcc.Graph(figure=fig_scatter),dcc.Graph(figure=fig_scatter2)]
        
        
    elif selected_value == 'causas':
        fig_bar = px.bar(
            df_death_cause_description.head(5), 
            x='id', 
            y='quantity', 
            hover_data=['description'],
            title='Causas da morte',
            labels={'id': 'Causas - CID', 'quantity': 'Quantidade de suicídos por', 'description': 'Motivo'}
            )
        figures = dcc.Graph(figure=fig_bar)
        
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