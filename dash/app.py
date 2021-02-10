import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np
import plotly.express as px
import datetime as dt

full_grouped = pd.read_csv("https://raw.githubusercontent.com/LuijiDarkSia/covid/main/data/full_grouped.csv")

'''
fig3 = px.choropleth(full_grouped, locations="countriesAndTerritories", locationmode='country names', color=np.log(full_grouped["cumsum_cases"]),
                    hover_name="countriesAndTerritories", animation_frame=full_grouped["dateRep"].dt.strftime('%Y-%m-%d'),
                    title='Reported Cases over time', color_continuous_scale=px.colors.sequential.Magenta)
fig3.update(layout_coloraxis_showscale=False)

'''
with urlopen('https://raw.githubusercontent.com/LuijiDarkSia/covid/main/data/landkreise_simplify0.geojson') as response:
    counties = json.load(response)

df = pd.read_csv("https://opendata.arcgis.com/datasets/917fc37a709542548cc3be077a786c17_0.csv")
df['RS'] = df['RS'].apply(str)
df['RS'] = df['RS'].str.zfill(5)

df_temp = df[400:]
df = df[:400]
list_temp = df_temp.mean(axis = 0, skipna = True)
list_temp["cases7_per_100k"] = df_temp["cases7_per_100k"].mean(axis = 0, skipna = True)
list_temp["RS"] = 11000
list_temp["GEN"] = "Berlin"
df.loc[len(df)] = list_temp

cumulated_data = pd.read_csv("https://covid19.who.int/WHO-COVID-19-global-table-data.csv")

geojson = counties
candidates = df["cases7_per_100k"]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

fig = px.choropleth(data_frame=df,
                    geojson=counties,
                    color='cases7_per_100k',
                    locations='RS',
                    featureidkey="properties.RS",
                    color_continuous_scale='viridis',
                    center={"lat": 51, "lon": 9},
                    hover_data=["GEN", "cases_per_100k", "death7_lk"],
                    projection="mercator")



fig.update_geos(fitbounds="locations", visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text']
)

cumulated_data_temp = cumulated_data[1:]

fig2 = px.choropleth(cumulated_data_temp, locations="Name", locationmode='country names', color='Cases - cumulative total per 1 million population', color_continuous_scale="inferno", range_color=(0, 100000), hover_name="Name", projection="orthographic")
fig2.update_layout(margin={"r":0,"t":0,"l":0,"b":0})


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Covid19 Dashboard World & Germany',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    html.Div(
        children='Data from RKI and John Hopkins',
        style={
        'textAlign': 'center',
        'color': colors['text']
    }),
    html.Div(
        children='Map Germany with Data on Landkreis Level',
        style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='choropleth_ger',
        figure=fig
    ),

    html.Div(
        children='Orthographic World Map with current Infections on country Level',
        style={
        'textAlign': 'center',
        'color': colors['text']
    }),

    dcc.Graph(
        id='choropleth_world',
        figure=fig2
    ),
'''
    dcc.Graph(
        id='choropleth_timeseries',
        figure=fig3
    )
'''
])

if __name__ == "__main__":
    app.run_server(debug=True)