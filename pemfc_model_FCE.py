from plotly.offline import download_plotlyjs, init_notebook_mode,  plot
import plotly.graph_objs as go
import math

traces = []

# considered current range [mA]
j_range = [i for i in range(1, 1000)]


# REVERSIBLE OCV [V]
E = 1.2


# PARAMETERS OF ACTIVATION LOSSES --------------------------------------------------------------------------------------
# constant A [V]
A = 0.06

# Exchange Current Density [mA/cm2]
j0 = 0.04

# PARAMETERS OF CROSSOVER LOSSES ---------------------------------------------------------------------------------------
# internal current [mA/cm²]
jn = 3

# PARAMETERS OF OHMIC LOSSES -------------------------------------------------------------------------------------------
# ohmic resitance [kOhm/cm²]
r = 0.0001

# PARAMETERS OF CONCENTRATION LOSSES -----------------------------------------------------------------------------------
# parameter m [V]
m = 0.00003

# parameter n [cm²/A]
n = 0.008

# THEORETICAL CELL VOLTAGE ---------------------------------------------------------------------------------------------

th_u_cell = []

for j in j_range:
    th_u_cell.append(E - j * r - A * math.log((j + jn) / j0) - m * math.exp(n * j))

traces.append(
    go.Scatter(x=j_range,
               y=th_u_cell,
               mode="lines",
               marker=dict(size=10, color='black'),
               name='all. losses',
               yaxis='y1'
               )
)

# traces.append(
#     go.Scatter(x=j_range,
#                y=th_u_cell,
#                mode="lines",
#                marker=dict(size=10, color='green'),
#                name='activation losses (CCL)',
#                yaxis='y1'
#                )
# )

# PLOTTTING
fig_data = traces

thn_potential = go.layout.Shape(type='line',
                                x0=min(j_range),
                                x1=max(j_range),
                                y0=1.48,
                                y1=1.48,
                                yref='y1',
                                line=dict(color='darkgrey', width=2, dash='dash'))

rev_potential = go.layout.Shape(type='line',
                                x0=min(j_range),
                                x1=max(j_range),
                                y0=1.23,
                                y1=1.23,
                                yref='y1',
                                line=dict(color='darkgrey', width=2))

fig = go.Figure(fig_data).update_layout(
    # TITLE
    title='POL-Theoretical',
    title_font=dict(size=30, color='black'),
    title_x=0.4,
    # XAXIS
    xaxis=dict(title='current density [A/cm²]',
               title_font=dict(size=24, color='black'),
               tickfont=dict(size=20, color='black'),
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
               title_font=dict(size=24, color='black'),
               tickfont=dict(size=20, color='black'),
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
               range=[0, 1.6]
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

plot(fig)
