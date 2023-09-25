from plotly.offline import download_plotlyjs, init_notebook_mode, plot
from pol_fitting import pemfc_pol_fce
import plotly.graph_objs as go


j = [j for j in range(1, 1000)]

A = [0.01* a for a in range(1, 25)]
r = [0.00001 * r for r in range(1, 1000, 100)]
m = [0.000001 * m for m in range(0, 51, 5)]
n = [0.01 * n for n in range(0, 51, 10)]

traces = []

# for a in A:
#     traces.append(pemfc_pol_fce(j_range=j, A=a, name='A='+str(a)))

# for r in r:
#     traces.append(pemfc_pol_fce(j_range=j, r=r, name='r='+str(r)))

for m in m:
    traces.append(pemfc_pol_fce(j_range=j, m=m, name='m='+str(m)))

# for n in n:
#     traces.append(pemfc_pol_fce(j_range=j, n=n, name='n='+str(n)))

# PLOT #################################################################################################################

fig = go.Figure(traces).update_layout(
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
               range=[0,100]
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

    # shapes=[rev_potential, thn_potential],

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