import math
import plotly.graph_objs as go

########################################################################################################################
# FIT OF POLARIZATION CURVE ACCORDING TO FUEL CELL SYSTEMS EXPLAINED
# PARAMETERS:
# j_range is range of considered current [mA]
# E is (theoretical) the reversible Open Circuit Potential [V]
# A is described by A = (R*T) / (2*alpha*F) where alpha is the charge-trasnfer-coefficent
# j0 is the exchange current density of the Electrode (more specifically the CCL) [mA/cm2]
# jn is the internal current (hydrogen crossover) [mA/cm2]
# r is the area specific ohmic/ionic resistance [kOhm]
# m & n are fitting parameters for the empirically derived term of mass transport overpotential [-}

# FITTING PARAMETERS:
# Activation Losses: A
# Ohmic Losses: r
# Concentration Losses: m, n

def pemfc_pol_fce(j_range,E_oc=1.2,A=0.06,r=0.0027,m=0.000035,n=0.11,name=''):

    trace_pol_th = []
    th_u_cell = []
    ocv_loss = []
    op_act = []
    op_ohm = []
    op_conc = []

    for j in j_range:

        th_u_cell.append(
            E_oc - A * math.log(j) - j * r - m * math.exp(n * j)
        )

        ocv_loss.append(
            E_oc
        )

        op_act.append(
            A*math.log(j)
        )

        op_ohm.append(
            j*r
        )

        op_conc.append(
            m*math.exp(n*j)
        )

    trace_pol_th.append(go.Scatter(x=j_range,
                              y=th_u_cell,
                              name=name + ' (all losses)',
                              mode="lines",
                              line=dict(width=2),
                              marker=dict(size=10, color='black'),
                              yaxis='y1'
                              )
                        )

    trace_pol_th.append(go.Scatter(x=j_range,
                              y=ocv_loss,
                              name=name + ' (ocv)',
                              mode="lines",
                              line=dict(width=1, dash='dot'),
                              marker=dict(size=10, color='black'),
                              yaxis='y1'
                              )
                        )

    trace_pol_th.append(go.Scatter(x=j_range,
                              y=op_act,
                              name=name + ' (act. losses)',
                              mode="lines",
                              line=dict(width=1),
                              marker=dict(size=10, color='green'),
                              yaxis='y1'
                              )
                        )

    trace_pol_th.append(go.Scatter(x=j_range,
                              y=op_ohm,
                              name=name + ' (ohm. losses)',
                              mode="lines",
                              line=dict(width=1),
                              marker=dict(size=10, color='blue'),
                              yaxis='y1'
                              )
                        )

    trace_pol_th.append(go.Scatter(x=j_range,
                              y=op_conc,
                              name=name + ' (conc. losses)',
                              mode="lines",
                              line=dict(width=1),
                              marker=dict(size=10, color='red'),
                              yaxis='y1'
                              )
                        )

    return trace_pol_th

########################################################################################################################
# FIT OF POLARIZATION CURVE ACCORDING TO FUEL CELL SYSTEMS EXPLAINED
# PARAMETERS:
# j_range is range of considered current [mA]
# b is the Tafel-Slope [-]

# FITTING PARAMETERS ###################################################################################################

# def pemfc_pol_kulikovsky(j_range,E=1.2,b=0.03,j0=):
#
#     for j in j_range:
#         u_th = b * math.arcsinh(((j0 / j_sigma) ** 2) / (2 * (c_h / c_ref) * (1 - math.exp(-j0 / (2 * j_star))))) \
#                + ((sigma_t * b ** 2) / (4 * F * D_ch)) * (
#                            (j0 / j - star) - math.log(1 + (j_0 ** 2 / (j_star ** 2 * beta ** 2)))) * (
#                            1 - (j0 / (jlim_star * (c_h / c_ref)))) ** -1 \
#                - b * math.log(1 - (j0 / (jlim_star * (c_h / c_ref))))