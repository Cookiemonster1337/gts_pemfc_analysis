from dash import Dash, dcc, html, Input, Output, callback
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
from pol_fitting import pemfc_pol_kulikovsky
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

app = Dash(__name__)

j = [j for j in range(1,400)]

colors = {'zbt':'#005EB8'}

app = Dash(external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([

    dcc.Graph(id='graph'),

    dcc.Slider(
        0.5, 1.48, 0.01,
        value=1.0,
        marks={i * 0.01: '{}'.format(round(i * 0.01, 2)) for i in range(50, 149, 10)},
        id='slider_Eoc',
        updatemode='drag',
    ),

    dcc.Slider(
        0, 0.1, 0.001,
        value=0.03,
        marks={i * 0.001: '{}'.format(round(i * 0.001, 2)) for i in range(1, 100, 10)},
        id='slider_b',
        updatemode='drag',
    ),

    dcc.Slider(
        0, 1, 0.01,
        value=0.126,
        marks={i * 0.01: '{}'.format(round(i * 0.01, 2)) for i in range(0, 100, 10)},
        id='slider_r',
        updatemode='drag',
    ),

    dcc.Slider(
        0, 0.001, 0.00001,
        value=0.817E-3,
        marks={i * 0.00001: '{}'.format(round(i * 0.00001, 2)) for i in range(0, 100, 10)},
        id='slider_ix',
        updatemode='drag',
    ),

    dcc.Slider(
        0, 0.001, 0.00001,
        value=1.36E-4,
        marks={i * 0.00001: '{}'.format(round(i * 0.00001, 2)) for i in range(0, 100, 10)},
        id='slider_D',
        updatemode='drag',
    ),

    dcc.Slider(
        0, 0.1, 0.001,
        value=0.0259,
        marks={i * 0.001: '{}'.format(round(i * 0.001, 2)) for i in range(0, 100, 10)},
        id='slider_Db',
        updatemode='drag',
    ),

    dcc.Slider(
        0, 0.1, 0.001,
        value=0.03,
        marks={i * 0.001: '{}'.format(round(i * 0.001, 2)) for i in range(0, 100, 10)},
        id='slider_sigma_t',
        updatemode='drag',
    ),


])

@callback(
    Output('graph', 'figure'),
    Input('slider_Eoc', 'value'),
    Input('slider_b', 'value'),
    Input('slider_r', 'value'),
    Input('slider_ix', 'value'),
    Input('slider_D', 'value'),
    Input('slider_Db', 'value'),
    Input('slider_sigma_t', 'value'),
)


def updateFigure(slider_Eoc, slider_b, slider_r, slider_ix, slider_D, slider_Db, slider_sigma_t):

    figure = figure=go.Figure(data=pemfc_pol_kulikovsky(E_oc=slider_Eoc,
                                                        b=slider_b,
                                                        r=slider_r,
                                                        i_x=slider_ix,
                                                        D=slider_D,
                                                        D_b=slider_Db,
                                                        sigma_t=slider_sigma_t,
                                                        )).update_layout(
    # TITLE
    # title='Polarization Curve Fit (acc. FCE)',
    # title_font=dict(size=30, color='black'),
    # title_x=0.5,
    # XAXIS
    xaxis=dict(title='current [mA]',
               title_font=dict(size=20, color='black'),
               tickfont=dict(size=16, color='black'),
               minor=dict(ticks="inside", ticklen=5, showgrid=False),
               gridcolor='lightgrey',
               griddash='dash',
               showline=True,
               zeroline=True,
               zerolinewidth=2,
               zerolinecolor='black',

               ticks='inside',
               ticklen=10,
               tickwidth=2,

               linewidth=2,
               linecolor='black',

               mirror=True,
               ),

    # YAXIS
    yaxis=dict(title='voltage [V]',
               title_font=dict(size=20, color='black'),
               tickfont=dict(size=16, color='black'),
               gridcolor='lightgrey',
               griddash='dash',
               minor=dict(ticks="inside", ticklen=5, showgrid=False),
               showline=True,
               zeroline=True,
               zerolinewidth=2,
               zerolinecolor='black',
               ticks='inside',
               ticklen=10,
               tickwidth=2,

               linewidth=2,
               linecolor='black',

               mirror=True,
               ),

    legend_font=dict(size=16),
    legend=dict(
        x=1.3,
        y=1,
        xanchor='right',  # Set the x anchor to 'right'
        yanchor='top',  # Set the y anchor to 'top'
        bgcolor="white",
        bordercolor="black",
        borderwidth=1,
    ),
    plot_bgcolor='white',
)
    return figure


app.run_server(debug=True)

