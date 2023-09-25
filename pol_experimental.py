
from plotly.offline import download_plotlyjs, init_notebook_mode, plot
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from pol_fitting import pemfc_pol_fce

file = r'dataframes\kcs#01_pol.csv'
palette = px.colors.qualitative.Bold

test_data_df = pd.read_csv(file, encoding='cp1252', low_memory=False)

test_data_df = test_data_df.sort_values(by='Time Stamp', ascending=True)

test_data_df = test_data_df[
    test_data_df['File Mark'].str.contains('polcurve_inc', na=False)
    |
    test_data_df['File Mark'].str.contains('polcurve_dec', na=False)
    ]

test_data_df['current rounded'] = round(test_data_df['current'], 2)

char_cycles = test_data_df['variable_20'].unique()

traces = []

cycle_df = test_data_df[test_data_df['variable_20'] == 1].reset_index(drop=True)
# cycle_df = test_data_df.reset_index(drop=True)
cycle_df = cycle_df.iloc[6:]

currents = cycle_df['current_set'].unique()
current_max = currents[-1]
currents = currents[:-1]

u_inc = []
u_dec = []

temp_inc = []
temp_dec = []

erry_inc = []
erry_dec = []

j = []

for current in currents:
    # DECREASING
    u_inc.append(cycle_df[(cycle_df['current_set'] == current) &
                          (cycle_df['File Mark'].str.contains('polcurve_inc', na=False))]['voltage'].mean())
    temp_inc.append(cycle_df[(cycle_df['current_set'] == current) &
                             (cycle_df['File Mark'].str.contains('polcurve_inc', na=False))][
                        'temp_cathode_endplate'].mean())
    erry_inc.append(cycle_df[(cycle_df['current_set'] == current) &
                             (cycle_df['File Mark'].str.contains('polcurve_inc', na=False))]['voltage'].std())

    # INCREASING
    u_dec.append(cycle_df[(cycle_df['current_set'] == current) &
                          (cycle_df['File Mark'].str.contains('polcurve_dec', na=False))]['voltage'].mean())
    temp_dec.append(cycle_df[(cycle_df['current_set'] == current) &
                             (cycle_df['File Mark'].str.contains('polcurve_dec', na=False))][
                        'temp_cathode_endplate'].mean())
    erry_dec.append(cycle_df[(cycle_df['current_set'] == current) &
                             (cycle_df['File Mark'].str.contains('polcurve_dec', na=False))]['voltage'].std())

    j.append(current / 25)

# J-MAX
u_inc.append(cycle_df[cycle_df['current_set'] == current_max]['voltage'].mean())
u_dec.append(cycle_df[cycle_df['current_set'] == current_max]['voltage'].mean())
erry_inc.append(cycle_df[cycle_df['current_set'] == current_max]['voltage'].std())
erry_dec.append(cycle_df[cycle_df['current_set'] == current_max]['voltage'].std())
temp_inc.append(cycle_df[cycle_df['current_set'] == current_max]['temp_cathode_endplate'].mean())
temp_dec.append(cycle_df[cycle_df['current_set'] == current_max]['temp_cathode_endplate'].mean())
j.append(current_max / 25)

traces.append(pemfc_pol_fce(j_range=j))
# traces_b = []
#
# test_data_df['duration/h'] = test_data_df.index * (1 / 60)
# time = test_data_df['duration/h']
# temp_cell = cycle_df['temp_cathode_endplate']
# voltage = cycle_df['voltage']
# current = cycle_df['current']
#
# traces_b.append(
#     go.Scatter(x=time,
#                y=voltage,
#                mode="lines",
#                name='Voltage [V]',
#                yaxis='y1'
#                )
# )
#
# traces_b.append(
#     go.Scatter(x=time,
#                y=current,
#                mode="lines",
#                name='Current [A]',
#                yaxis='y2'
#                )
# )
#
# traces_b.append(
#     go.Scatter(x=time,
#                y=temp_cell,
#                mode="lines",
#                name='Cell Temperature [°C]',
#                yaxis='y2'
#                )
# )

traces.append(
    go.Scatter(x=j,
               y=u_inc,
               mode="markers+lines",
               marker=dict(size=10, color='red'),
               error_y=dict(array=erry_inc, thickness=1),
               name='pol inc.',
               yaxis='y1'
               )
)
#
# traces.append(
#     go.Scatter(x=j,
#                y=u_dec,
#                mode="markers+lines",
#                marker=dict(size=10, color='blue'),
#                error_y=dict(array=erry_dec, thickness=1),
#                name='pol dec.',
#                yaxis='y1'
#                )
# )
#
# traces.append(
#     go.Scatter(x=j,
#                y=temp_inc,
#                mode="markers+lines",
#                marker=dict(size=10, color='red'),
#                line=dict(dash='dash'),
#                name='temp inc.',
#                yaxis='y2'
#                )
# )
#
# traces.append(
#     go.Scatter(x=j,
#                y=temp_dec,
#                mode="markers+lines",
#                marker=dict(size=10, color='blue'),
#                line=dict(dash='dash'),
#                name='temp dec.',
#                yaxis='y2'
#                )
# )

# AVERAGE POL

currents = test_data_df['current_set'].unique()

u = []
j = []
erry = []
errx = []

for current in currents:
    if current < 46:
        u.append(test_data_df[test_data_df['current_set'] == current]['voltage'].mean())
        j.append(current/25)
        erry.append(test_data_df[test_data_df['current_set'] == current]['voltage'].std())
        errx.append(0)

u.append(test_data_df[test_data_df['current_set'] > 45]['voltage'].mean())
j.append(test_data_df[test_data_df['current_set'] > 45]['current'].mean()/25)
erry.append(test_data_df[test_data_df['current_set'] > 45]['voltage'].std())
errx.append(test_data_df[test_data_df['current_set'] > 45]['current'].std()/25)


# traces.append(
#     go.Scatter(x=j, y=u, mode="markers+lines",
#                marker=dict(size=10, color='black'),
#                error_y=dict(array=erry, thickness=1),
#                error_x=dict(array=errx, thickness=1),
#                name='POL Average', )
#     )


fig_a_data = traces

target_temp = go.layout.Shape(type='line',
                              x0=min(j),
                              x1=2,
                              y0=85,
                              y1 =85,
                              yref='y2',
                              line=dict(color='darkgrey', width=2))

fig_a = go.Figure(fig_a_data).update_layout(
                        # TITLE
                        title='POL-Analysis',
                        title_font=dict(size=30, color='black'),
                        title_x=0.4,
                        #XAXIS
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
                                   # range=[0, 0.2]
                                   ),

                        #YAXIS
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
                                   # range=[0.8, 1.2]
                                   ),

                        # yaxis2=dict(title='Temperature [°C]',
                        #             overlaying='y',
                        #             side='right',
                        #             title_font=dict(size=24, color='black'),
                        #             tickfont=dict(size=20, color='black'),
                        #             minor=dict(ticks="inside", ticklen=5, showgrid=False),
                        #             ticks='inside',
                        #             ticklen=10,
                        #             tickwidth=2,
                        #
                        #             linewidth=2,
                        #             linecolor='black',
                        #             range=[0, 100],
                        #             ),
                        #             shapes=[target_temp],

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


plot(fig_a)

# fig_b_data = traces_b
#
# target_temp = go.layout.Shape(type='line',
#                               x0=min(j),
#                               x1=2,
#                               y0=85,
#                               y1=85,
#                               yref='y2',
#                               line=dict(color='darkgrey', width=2))
#
# fig_b = go.Figure(fig_b_data).update_layout(
#     # TITLE
#     title='POL-Analysis',
#     title_font=dict(size=30, color='black'),
#     title_x=0.4,
#     # XAXIS
#     xaxis=dict(title='duration',
#                title_font=dict(size=24, color='black'),
#                tickfont=dict(size=20, color='black'),
#                minor=dict(ticks="inside", ticklen=5, showgrid=False),
#                gridcolor='lightgrey',
#                griddash='dash',
#                showline=True,
#                zeroline=True,
#                zerolinewidth=2,
#                zerolinecolor='black',
#
#                ticks='inside',
#                ticklen=10,
#                tickwidth=2,
#
#                linewidth=2,
#                linecolor='black',
#
#                mirror=True,
#                ),
#
#     # YAXIS
#     yaxis=dict(title='voltage [V]',
#                title_font=dict(size=24, color='black'),
#                tickfont=dict(size=20, color='black'),
#                gridcolor='lightgrey',
#                griddash='dash',
#                minor=dict(ticks="inside", ticklen=5, showgrid=False),
#                showline=True,
#                zeroline=True,
#                zerolinewidth=2,
#                zerolinecolor='black',
#                ticks='inside',
#                ticklen=10,
#                tickwidth=2,
#
#                linewidth=2,
#                linecolor='black',
#
#                mirror=True,
#                ),
#
#     yaxis2=dict(title='Temperature [°C]',
#                 overlaying='y',
#                 side='right',
#                 title_font=dict(size=24, color='black'),
#                 tickfont=dict(size=20, color='black'),
#                 minor=dict(ticks="inside", ticklen=5, showgrid=False),
#                 ticks='inside',
#                 ticklen=10,
#                 tickwidth=2,
#
#                 linewidth=2,
#                 linecolor='black',
#                 ),
#     shapes=[target_temp],
#
#     legend_font=dict(size=16),
#     legend=dict(
#         x=1.3,
#         y=1,
#         xanchor='right',  # Set the x anchor to 'right'
#         yanchor='top',  # Set the y anchor to 'top'
#         bgcolor="white",
#         bordercolor="black",
#         borderwidth=1,
#     ),
#     plot_bgcolor='white',
# )

# plot(fig_b)