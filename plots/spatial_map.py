import pandas as pd
import numpy as np
import plotly.graph_objs as go
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
from plots.util import *

# map figure
mapbox_access_token = "pk.eyJ1IjoiZ291bGRzYnIiLCJhIjoiY2tiOTJzd2MwMGExdDJ6cGk3azl3cmM1dyJ9.lNyqUkLC-tMglqst6vmUBw"
morcombe_bay = (54.1166662, -3.0)
mid_scotland = (55.64, -3.625)

default_date = pd.to_datetime('01/01/2020', format="%d/%m/%Y")


def create_map_figure(location=None, pollutant='o3', date=default_date):
    print('updating map...', location, pollutant, date)
    pollutant = f'{pollutant}_mean'

    headers = list(diff_df.keys())
    code_lat_lng = meta_df[['code', 'latitude', 'longitude']].values
    u, idx = np.unique(code_lat_lng[:, 0], return_index=True)
    code_to_latlng = {code: {'lat': lat, 'lng': lng} for code, lat, lng in code_lat_lng[idx]}

    data_vals = diff_df[['location', pollutant, 'date']]
    data_vals = data_vals[data_vals['date'] == date]
    data_vals = data_vals.dropna()

    site_lat = np.array([code_to_latlng[loc]['lat'] for loc in data_vals['location']])
    site_lng = np.array([code_to_latlng[loc]['lng'] for loc in data_vals['location']])

    fig = go.Figure()
    cmin = min_max_dict[pollutant]['min']
    cmax = min_max_dict[pollutant]['max']

    if location is None:
        loc = dict(lat=mid_scotland[0], lon=mid_scotland[1])
        z = 4
    else:
        loc = dict(lat=code_to_latlng[location]['lat'],
                   lon=code_to_latlng[location]['lng'])
        z = 8
        fig.add_trace(go.Scattermapbox(lat=[loc['lat']],
                                       lon=[loc['lon']],
                                       mode='markers',
                                       marker=go.scattermapbox.Marker(
                                               size=20,
                                               cmin=cmin,
                                               cmax=cmax,
                                               color='rgb(0,0,0)',
                                               opacity=1,
                                               showscale=True,
                                               colorscale="Geyser",
                                       ),
                                       text=location,
                                       hoverinfo='none'))

    fig.add_trace(go.Scattermapbox(lat=site_lat,
                                   lon=site_lng,
                                   mode='markers',
                                   marker=go.scattermapbox.Marker(
                                           size=17,
                                           cmin=cmin,
                                           cmax=cmax,
                                           color=data_vals[pollutant].values.astype(np.float),
                                           opacity=.93,
                                           showscale=True,
                                           colorscale="Geyser"
                                   ),
                                   text=u,
                                   hoverinfo='text'
                                   ))

    fig.update_layout(
            # title='Title',
            autosize=True,
            hovermode='closest',
            margin=dict(t=0, b=0, l=0, r=0),
            showlegend=False,
            mapbox=dict(
                    accesstoken=mapbox_access_token,
                    bearing=0,
                    center=loc,
                    pitch=0,
                    zoom=z,
                    style='light',
            ),
            # paper_bgcolor='rgb(0,0,0,0)'
    )
    return fig


if __name__ == '__main__':
    map_view = create_map_figure()
    map_view.show()
