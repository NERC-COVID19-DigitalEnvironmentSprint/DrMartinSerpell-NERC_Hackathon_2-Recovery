import dash_core_components as dcc
import dash_html_components as html
from plots.util import *
from plots.mobility import create_mobility_figure
from plots.energy_usage import create_energy_figure
from plots.rm_weather import create_rm_weather_figure
from plots.spatial_map import create_map_figure


def title():
    return html.H1("What can we learn from lockdown?", className='title prose')


def title1():
    t1 = html.H1("Trends in air pollution", className='title prose')
    intro = html.P(["In order to reach net zero emmisions by 2050, reductions in emissions and air pollutants "
                    "must continue to reduce at rates similar if not more drastically than what has been "
                    "observed during lockdown. ", html.Br(), html.Br(), "The "
                                                                        "Automatic Urban and Rural Network (AURN) provide hourly "
                                                                        "measurements of air pollutants "
                                                                        "from across the UK. ", html.Br(),
                    "Multivariate signals were used to reduce the day to day variability "
                    "of pollutants NO2, O3, PM10 and PM2.5 in order to view their underlying behaviour.", html.Br(),
                    " Meteorological normalisation "
                    "applied to pollutant data for 2020 highlights the impact that lockdown has had on air quality "
                    "within the UK. ", html.Br(),
                    "The signals removed include: air temperature, wind speed, wind direction, "
                    "day of year, day of week and hour of day. This analysis was performed using the "
                    "rmweather package. ", html.Br(), html.Br(),
                    " Select a location from the drop down below to see how air pollution "
                    "has changed due to lockdown. ", html.Br(), "You can drag and zoom the map to view the normalised "
                                                                "daily mean pollutant level spatially across the UK. ",
                    html.Br(),
                    "NOTE: AURN data for 2020 is yet to be ratified."], className='prose')
    box = html.Div([t1, intro], id='title_section2')
    return box


def title2():
    t1 = html.H1("Paris Net Zero", className='title prose')
    intro = html.P(["In order to reach net zero emissions by 2050, huge changes must be made"
                    "from across the UK.", html.Br(),
                    "Multivariate signals were used to reduce the day to day variability "
                    "of each pollutant in order to view their underlying behaviour.", html.Br(),
                    " Meteorological normalisation "
                    "applied to pollutant data for 2020 highlights the impact that lockdown has had on air quality "
                    "within the UK. ", html.Br(),
                    "The signals removed include: air temperature, wind speed, wind direction, "
                    "day of year, day of week and hour of day. This analysis was performed using the "
                    "rmweather package. ", html.Br(),
                    " Select a location from the drop down below to see how air pollution "
                    "has changed due to lockdown. ", html.Br(), "You can drag and zoom the map to view the normalised "
                                                                "daily mean pollutant level spatially across the UK. ",
                    html.Br(),
                    "NOTE: AURN data for 2020 is yet to be ratified."], className='prose')
    box = html.Div([t1, intro], id='title_section3')
    return box


def subtitle():
    return html.P("  The nationwide lockdown has led to improved air "
                  "quality and reduced emissions across the UK.", id='subtitle', className='prose')


def plot_mobility():
    return dcc.Graph(figure=create_mobility_figure(), id='mobility_plot', className='figure', responsive=True)


def plot_energy_usage():
    return dcc.Graph(figure=create_energy_figure(), id='energy_plot', className='figure', responsive=True)


def mobility_energy():
    txtb0 = html.P(["Drastic reductions in driving and transit behaviour were seen once lockdown came into effect. "
                    "An increase in driving mobility can be observed once the lockdown guidance "
                    "changed from 'STAY AT HOME, PROTECT THE NHS, SAVE LIVES' to 'STAY ALERT, "
                    "CONTROL THE VIRUS, SAVE LIVES' when lockdown measures began to be eased.", html.Br(), html.Br(),
                    "Data is from Apple mobility."],
                   id='txtb_mobility_energy_0', className='prose textb')

    txtb1 = html.P(["Energy consumption for March decreased by ~2% for inland UK. Wind, solar "
                    "and hydro fuel consumption increased by by ~6.5%.", html.Br(), html.Br(),
                    "Data is from Department for Business, Energy & Industrial Strategy."],
                   id='txtb_mobility_energy_1', className='prose textb')

    c1 = html.Div([txtb0, plot_mobility()], className='pretty_container five columns')
    c2 = html.Div([txtb1, plot_energy_usage()], className='pretty_container five columns')

    me = [c1, c2]
    return html.Div(me, id='mobility_energy', className='fig_container')


def pollutant_select(pollutants=None):
    default_pollutants = ['no2', 'o3', 'pm10', 'pm2.5']
    if pollutants is None:
        pollutants = default_pollutants

    ps = dcc.RadioItems(
            options=[{'label': pol, 'value': pol} for pol in pollutants],
            value=pollutants[0],
            labelStyle={'display': 'inline-block'},
            persistence=False,
            className='flex-item',
            id='pollutant_select')

    return ps


def location_select(pollutant=None):
    ls = dcc.Dropdown(
            options=[{'label': site, 'value': code} for code, site in get_locations().values],
            placeholder="Default location: Manchester Piccadilly",
            persistence=False,
            className='flex-item',
            id='location_select')
    return ls


def selectors_loc_pollutant():
    return html.Div([location_select(), pollutant_select()], id='location_pollutant', className='flex-row')


def pollutant_info(location=None, pollutant=None):
    wf = dcc.Graph(figure=create_rm_weather_figure(location, pollutant), id='rm_weather_plot', className='figure',
                   responsive=True)

    mf = dcc.Graph(figure=create_map_figure(), id='map_plot', className='figure', responsive=True)

    wf_mf = html.Div([wf, mf], id='pollutant_plot', className='fig_container')

    interval = dcc.Interval(id='auto-stepper',
                            interval=4 * 1000,  # in milliseconds
                            n_intervals=0,
                            max_intervals=len(dates),
                            disabled=True
                            )

    buttons = html.Div([
        html.Button('Play', id='btn_play', n_clicks=0),
        html.Button('Stop', id='btn_stop', n_clicks=0),
        html.Div(id='container-button-timestamp'),
        interval
    ])

    date_widg = html.Div([
        date_slider(),
        # buttons
    ])

    return html.Div([selectors_loc_pollutant(), wf_mf, date_widg], id='pollutant_info')


weeks = {i: {'label': dmarks[i].split(' ')[0]} for i in range(len(dmarks))}
weeks[11] = {'label': weeks[11]['label'], 'style': {'color': '#f50'}}


def date_slider():
    ds = dcc.Slider(marks=weeks,
                    min=-1,
                    max=len(dmarks),
                    value=0,
                    updatemode='mouseup',
                    persistence=False,
                    id='date_slider',
                    )
    return ds
