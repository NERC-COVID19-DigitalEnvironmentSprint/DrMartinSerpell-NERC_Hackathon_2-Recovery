import plotly.express as px
from plots.util import *


def create_energy_figure():
    df = load_data('consumption_change.csv')
    fig = px.bar(df, x='fuel', y='change', color='change', color_continuous_midpoint=0,
                 color_continuous_scale=px.colors.diverging.Tealrose, range_color=[-45, 20])

    fig.update_layout(
            margin=dict(t=0, b=0, l=0, r=0),
            xaxis_title="Fuel",
            yaxis_title="% Change in consumption",
    )
    return fig


if __name__ == '__main__':
    data = create_energy_figure()
    data.show()
