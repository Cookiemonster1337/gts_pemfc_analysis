import math
import plotly.graph_objs as go


def pemfc_pol_fce(j_range,E=1.2,A=0.06,j0=0.04,jn=2.5,r=0.0027,m=0.000035,n=0.11):

    th_u_cell = []

    for j in j_range:
        j = j/25*1000
        th_u_cell.append(E - j * r - A * math.log((j + jn) / j0) - m * math.exp(n * j))

    trace_pol_th = go.Scatter(x=j_range,
                   y=th_u_cell,
                   mode="lines+markers",
                   marker=dict(size=10, color='green'),
                   name='act + co + ohmic loss + conc. loss.',
                   yaxis='y1'
                   )


    return trace_pol_th