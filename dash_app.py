import dash
import dash_core_components as dcc
import dash_html_components as html
from pathlib import Path
from components import *
from plots.mobility import create_mobility_figure
from dash.dependencies import Input, Output, State, ClientsideFunction

PATH = Path(__file__).parent

app = dash.Dash(__name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}])

main_container = [
    title(),
    subtitle(),
    mobility_energy(),
    title1(),
    pollutant_info(),
]


@app.callback([Output('rm_weather_plot', 'figure'),
               Output('map_plot', 'figure')],
              [Input('location_select', 'value'),
               Input('pollutant_select', 'value'),
               Input('date_slider', 'value')])
def updates(location, pollutant, date):
    print(location, pollutant, date)
    date = pd.to_datetime(get_datemarks(date))
    return create_rm_weather_figure(location, pollutant), create_map_figure(location, pollutant, date)
    # date), f"{date.strftime('%d-%m-%Y')}"


@app.callback([Output('location_select', 'options')],
              [Input('pollutant_select', 'value')])
def update_location(pollutant):
    if pollutant is None:
        return [{'label': site, 'value': code} for code, site in get_locations().values]

    pollutant = f'{pollutant}_mean'
    new_options = [{'label': site, 'value': code} for code, site in get_locations().values if
                   code in get_available_locs(pollutant)]
    print('new options =', len(new_options))
    return [new_options]


# @app.callback([Output('container-button-timestamp', 'children'),
#                Output('auto-stepper', 'disabled')],
#               [Input('btn_play', 'n_clicks'),
#                Input('btn_stop', 'n_clicks')])
# def displayClick(btn1, btn2):
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     play = True
#     if 'btn_play' in changed_id:
#         msg = f'Start Button clicked'
#         play = False
#     elif 'btn_stop' in changed_id:
#         msg = 'Stop Button clicked'
#     else:
#         msg = 'None of the buttons have been clicked yet'
#     return html.Div(msg), play


# @app.callback(Output('date_slider', 'value'),
#               [Input('auto-stepper', 'n_intervals')])
# def on_click(n_intervals):
#     print(n_intervals, '/', len(dmarks))
#     if n_intervals is None:
#         return 0
#     if n_intervals == 0:
#         return 0
#     else:
#         return [(n_intervals + 1) % len(dmarks)]


app.layout = html.Div(main_container, id='main_container')

if __name__ == '__main__':
    app.run_server()
