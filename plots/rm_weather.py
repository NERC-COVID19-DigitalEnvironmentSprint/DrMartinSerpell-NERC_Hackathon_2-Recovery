import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plots.util import *


def create_rm_weather_figure(location=None, pollutant=None):
    print('updating rm weather figure...', location, pollutant)
    if pollutant is None:
        pollutant = 'o3'
    if location is None:
        location = 'MAN3'

    df = load_data('ALL_rm_daily_2.csv')
    df.dropna(axis=1, how='all', inplace=True)
    df = df.replace('nan', np.nan, regex=True)

    df = df.loc[df['location'] == location]

    to_plot = [x for x in list(df.keys()) if pollutant in x]

    fig = go.Figure()
    names = {f'{pollutant}_max': 'Normalised Max',
             f'{pollutant}_raw_max': 'Raw Max',
             f'{pollutant}_min': 'Normalised Min',
             f'{pollutant}_raw_min': 'Raw Min',
             f'{pollutant}_mean': 'Normalised Mean',
             f'{pollutant}_raw_mean': 'Raw Mean'}

    fig.add_traces([go.Scatter(x=df['date'], y=df[header], name=names[header], mode='lines') for i, header in
                    enumerate(to_plot)])

    fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            xaxis_title="Date",
            yaxis_title="Level of pollutant (ug/m3)",
    )
    return fig


if __name__ == '__main__':
    plot = create_rm_weather_figure('no2')
    plot.show()
