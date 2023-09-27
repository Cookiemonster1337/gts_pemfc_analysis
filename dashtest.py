from dash import Dash, dcc, html, Input, Output, callback
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
from pol_fitting import pemfc_pol_fce
import plotly.graph_objs as go
import dash_bootstrap_components as dbc

app = Dash(__name__)

j = [j for j in range(1,400)]

colors = {'zbt':'#005EB8'}

app = Dash()

app.layout = dbc.Container([

# TITLE
    dbc.Row([
        html.Div(['Polarization Curve Fitting'
                  ], style={'font-family': 'Arial',
                      'font-size': '16px',
                      'font-weight': 'bold',
                      'textAlign': 'center',
                      'color': 'black'}
                 ),
    ], style={'background-color': 'white'}),

# PLOT OF POLARIZATION-CURVE MODEL (according to FCE)
    dbc.Row([
        dcc.Graph(id='graph'),
    ], style={'background-color': 'white'}),

# SLIDER - OPEN CIRCUIT POTENTIAL
    dbc.Row([
        dbc.Col([
            html.Div([
                'Open Circuit Potential (E_oc)'
            ], style={'font-family': 'Arial',
                      'font-size': '12px',
                      'font-weight': 'bold',
                      'textAlign': 'center',
                      'color': 'black'}
            )

        ], width=3, style={'background-color': 'white'}),

        dbc.Col([

            dcc.Slider(
                0.5, 1.48, 0.01,
                value=1.0,
                marks={i*0.01: '{}'.format(round(i*0.01,2)) for i in range(50,149,10)},
                id='slider_Eoc',
                updatemode='drag',
            )

        ], width=9, style={'background-color': 'white'}),

    ], style={'background-color': 'white'}, align='center'),

# SLIDER - CCL ACTIVITY
    dbc.Row([

        dbc.Col([

            html.Div([
                'Activity Coefficent (*)'
            ], style={'font-family': 'Arial',
                      'font-size': '12px',
                      'font-weight': 'bold',
                      'textAlign': 'center',
                      'color': 'black'})

        ], width=3, style={'background-color': 'white'}),

        dbc.Col([

            dcc.Slider(
                0, 0.25, 0.01,
                value=0.06,
                id='slider_A',
                updatemode='drag',
                # tooltip={"placement": "bottom", "always_visible": True},
            ),

        ], width=9, style={'background-color': 'white'}),

    ], align='center', style={'background-color': 'white'}),

    # SLIDER - AREA SPECIFIC RESISTANCE [kOhm]
    dbc.Row([

        dbc.Col([

           html.Div([
                'Area Specific Resistance'
            ], style={'font-family': 'Arial',
                      'font-size': '12px',
                      'font-weight': 'bold',
                      'textAlign': 'center',
                      'color': 'black'})

        ], width=3, style={'background-color': 'white'}),

        dbc.Col([

            dcc.Slider(
                0, 0.01, 0.0001,
                id='slider_r',
                marks={i * 0.001: '{}'.format(round(i * 0.001, 3)) for i in range(0, 11)},
                # tooltip={"placement": "bottom", "always_visible": True},
                value=0.002,
                updatemode='drag'
            ),

        ], width=9, style={'background-color': 'white'}),

    ], align='center', style={'background-color': 'white'}),

    # SLIDER - AREA SPECIFIC RESISTANCE [kOhm]
    dbc.Row([

        dbc.Col([

            html.Div([
                'Mass Transport Parameter (m)'
            ], style={'font-family': 'Arial',
                      'font-size': '12px',
                      'font-weight': 'bold',
                      'textAlign': 'center',
                      'color': 'black'}
            )

        ], width=3, style={'background-color': 'white'}),

        dbc.Col([

            dcc.Slider(
                0, 0.00005, 0.000001,
                id='slider_m',
                marks={i * 0.000001: '{}'.format(round(i * 0.000001, 6)) for i in range(0, 51, 10)},
                # tooltip={"placement": "bottom", "always_visible": True},
                value=0.000015,
                updatemode='drag'
                ),

        ], width=9, style={'background-color': 'white'}),

    ], align='center', style={'background-color': 'white'}),

    # SLIDER - AREA SPECIFIC RESISTANCE [kOhm]
    dbc.Row([

        dbc.Col([

            html.Div([
                'Mass Transport Parameter (n)'
            ], style={'font-family': 'Arial',
                      'font-size': '12px',
                      'font-weight': 'bold',
                      'textAlign': 'center',
                      'color': 'black'})

        ], width=3, style={'background-color': 'white'}),

        dbc.Col([

            dcc.Slider(
                0, 0.5, 0.01,
                id='slider_n',
                marks={i * 0.01: '{}'.format(round(i * 0.01, 2)) for i in range(0, 51, 5)},
                value=0.1,
                updatemode='drag'
            ),

        ], width=9, style={'background-color': 'white'}),

    ], align='center', style={'background-color': 'white'}),

],
)

@callback(
    Output('graph', 'figure'),
    Input('slider_Eoc', 'value'),
    Input('slider_A', 'value'),
    Input('slider_r', 'value'),
    Input('slider_m', 'value'),
    Input('slider_n', 'value')
)

def updateFigure(
        slider_Eoc,
        slider_A,
        slider_r,
        slider_m,
        slider_n
):
    thn_potential = go.layout.Shape(type='line',
                                    x0=min(j),
                                    x1=max(j),
                                    y0=1.48,
                                    y1=1.48,
                                    yref='y1',
                                    line=dict(color='black', width=1))

    rev_potential = go.layout.Shape(type='line',
                                    x0=min(j),
                                    x1=max(j),
                                    y0=1.23,
                                    y1=1.23,
                                    yref='y1',
                                    line=dict(color='black', width=1, dash='dash'))

    figure = figure=go.Figure(data=pemfc_pol_fce(j_range=j,
                                                 E_oc=slider_Eoc,
                                                 A=slider_A,
                                                 r=slider_r,
                                                 m=slider_m,
                                                 n=slider_n
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
               range=[0, 1.5]
               ),

    shapes=[rev_potential, thn_potential],

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

# app.css.append_css({
#     'external_url': 'custom.css'}
# )


app.run_server(debug=True)


# traces = []
#
# traces.append(pemfc_pol_fce(j_range=j, m=m, name='m='+str(m)))