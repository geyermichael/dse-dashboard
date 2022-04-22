# DSE Dashboard
# Author Michael Geyer

# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import pandas as pd
import requests

app = Dash(__name__)

# Liste an Jahren
years = [*range(2016, 2022, 1)]

# Erzeuge Dashboard im Browser
app.layout = html.Div(children=[
    
    html.Div(children=(
        
    # Header
    html.Header(children=(
        html.H1(children="Dashboard"),
        html.H3(children="Wirtschaftsdaten der Stadt München"),
        html.P(children="Datenquelle: https://opendata.muenchen.de/dataset/monatszahlen-wirtschaft"),
        html.P(children="Author: Michael Geyer"),
        ),
    className='header'
    ),
    
    # Main Content
    html.Div([
        dcc.Graph(
        id='bar-chart',
        responsive=False,
    ),
        html.H4(children="Jahr"),
        dcc.Dropdown(
        id="bar-choose-year",
        options=years,
        value="2020",
        clearable=False,
    ),]),
    
    html.Div([
        dcc.Graph(
        id='line-chart',
        responsive=False,
    ),
        html.H4(children="Jahr"),
        dcc.Dropdown(
        id="line-choose-year",
        options=years,
        value="2020",
        clearable=False,
    ),]), 
    ), 
    className='dashboard'),
     
])

# Request an die API mit einer entsprechendne query.
# Gibt den response zurück.
def get_data(query):
    api_base = f'https://opendata.muenchen.de/api/3/action/datastore_search?q='
    api_resource_id = '&resource_id=cdf75551-993c-4410-8621-2709400629eb'
    response = requests.get(api_base + query + api_resource_id)
    data = response.json()
    data = data['result']['records']

    return data

# Interaktion für das BarChart (Gesamtumsatz)
@app.callback(
    Output("bar-chart", "figure"), 
    Input("bar-choose-year", "value"))
def update_bar_chart(year):
    data = get_data(query=f'{year},"Verarbeitendes Gewerbe",Gesamtumsatz')
    
    df = pd.DataFrame(data)
    # lösche Einträge aus df die in der Spalte "MONAT" den Wert "Summe" besitzen
    df.drop(df[df['MONAT'] == "Summe"].index, inplace = True) 

    fig = px.bar(
        df, 
        x="MONAT", 
        y="WERT", 
        title="Gesamtumsatz in EUR des verarbeitenden Gewerbes",)
    
    return fig

# Interaktion für das LineChart (Anzahl Beschäftige)        
@app.callback(
    Output("line-chart", "figure"), 
    Input("line-choose-year", "value"))
def update_bar_chart(year):
    data = get_data(query=f'{year},"Verarbeitendes Gewerbe",Beschäftigte')
    
    df = pd.DataFrame(data)

    fig = px.line(
        df, 
        x="MONAT", 
        y="WERT",  
        title="Anzahl der Beschäftigten des verarbeitenden Gewerbes",
        markers=True,)
    
    return fig
    
# Run server
if __name__ == '__main__':
    app.run_server(debug=True)


