import pandas as pd
import datetime
import plotly.graph_objects as go
from plots.util import *

df = load_data("apple_mobility.csv", datetime_format="%d/%m/%Y")
df2 = load_data("aviation_reduction.csv", datetime_format="%d/%m/%Y")

# _df = pd.date_range(start='1/1/2020', end='15/06/2020')


def create_mobility_figure():
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=df['date'], y=df['t'],
                             name='Transit',
                             line=dict(color='cornflowerblue', width=2.5)))

    fig.add_trace(go.Scatter(x=df['date'], y=df['d'],
                             name='Driving',
                             line=dict(color='palevioletred', width=2.5)))

    # fig.add_trace(go.Scatter(x=df2['date'], y=df2['reduction'],
    #                          name='Scheduled flights',
    #                          line=dict(color='royalblue', width=2.5,
    #                                    shape='linear')))

    x_mark = pd.to_datetime('23/03/2020', format="%d/%m/%Y")

    fig.add_shape(dict(
            type="line",
            x0=x_mark,
            y0=-100,
            x1=x_mark,
            y1=40,
            line=dict(color="grey", width=3)))

    x_mark = pd.to_datetime('10/05/2020', format="%d/%m/%Y")
    fig.add_shape(dict(
            type="line",
            x0=x_mark,
            y0=-100,
            x1=x_mark,
            y1=40,
            line=dict(color="darkgrey", width=3)))

    t1 = ["Start of lockdown", "Advice change"]
    t2 = [pd.to_datetime('25/03/2020', format="%d/%m/%Y"),
          pd.to_datetime('12/05/2020', format="%d/%m/%Y")]
    fig.update_layout(annotations=[
        go.layout.Annotation(x=datepoint,
                             xref="x",
                             yref="y",
                             text=txt,
                             align='center',
                             showarrow=False,
                             yanchor='middle',
                             textangle=90) for datepoint, txt in zip(t2, t1)])

    fig.update_xaxes(nticks=22)
    fig.update_traces(texttemplate='%{text:.2s}')
    fig.update_layout(xaxis=dict(tickformat='%d-%m'),
                      xaxis_title="Date",
                      yaxis_title="% Change in mobility",
                      margin=dict(t=0, b=0, l=0, r=0),
                      )

    # fig.add_trace(go.Scatter(x="gdpPercap", y="lifeExp", color="continent", trendline="lowess"))
    return fig


if __name__ == '__main__':
    mobility_fig = create_mobility_figure()
    mobility_fig.show()
