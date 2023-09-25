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

def pemfc_pol_kulikovsky(j_range=[j for j in range(1, 2000)],
                         b=0.03,
                         r=0.126,
                         D=1.36E-4,
                         sigma_t=0.03,
                         E_oc=1.145,
                         c_h=7.36E-6,
                         i_x = 0.817E-3,
                         l_t = 0.001,
                         D_b = 0.0259,
                         l_b = 0.025,
                         name=''):

    trace_pol_th=[]
    u_th = []
    loss_ohm = []
    loss_act = []

    c_h_x = c_h
    c_ref = c_h
    F = 96485
    j_sigma = math.sqrt(2*i_x *sigma_t * b)
    j_x = (sigma_t * b) / l_t
    jlim_x = ((4*F*D_b*c_h_x)/l_b)

    for j in j_range:

        j_0 = j/1000

        beta = (math.sqrt(2 * j_0) / (1 + math.sqrt(1.12 * j_0) * math.exp(math.sqrt(2 * j_0)))) + (math.pi * j_0) / (
                    2 + j_0)

        u_loss = b * math.asinh(((j_0 / j_sigma) ** 2) / (2 * (c_h / c_ref) * (1 - math.exp(-j_0 / (2 * j_x))))) \
               + ((sigma_t * b ** 2) / (4 * F * D * c_h)) * ((j_0 / j_x) - math.log(1 + (j_0 ** 2 / (j_x** 2 * beta ** 2)))) * (1 - (j_0 / (jlim_x * (c_h / c_ref)))) ** -1 \
               - b * math.log(1 - (j_0 / (jlim_x * (c_h / c_ref))))

        loss_ohm.append(r*j_0)

        loss_act.append(u_loss)

        u_th.append(E_oc - u_loss - r*j_0)

    trace_pol_th.append(go.Scatter(x=j_range,
                                   y=u_th,
                                   name=name + ' (curve)',
                                   mode="lines",
                                   line=dict(width=1),
                                   marker=dict(size=10, color='red'),
                                   yaxis='y1'
                                   )
                        )

    trace_pol_th.append(go.Scatter(x=j_range,
                                   y=loss_ohm,
                                   name=name + ' (ohm. losses)',
                                   mode="lines",
                                   line=dict(width=1),
                                   marker=dict(size=10, color='blue'),
                                   yaxis='y1'
                                   )
                        )

    trace_pol_th.append(go.Scatter(x=j_range,
                                   y=loss_act,
                                   name=name + ' (act. losses)',
                                   mode="lines",
                                   line=dict(width=1),
                                   marker=dict(size=10, color='green'),
                                   yaxis='y1'
                                   )
                        )

    trace_pol_th.append(go.Scatter(x=[0],
                                   y=[E_oc],
                                   name=name + ' (OCV)',
                                   mode="markers",
                                   line=dict(width=1),
                                   marker=dict(size=10, color='red'),
                                   yaxis='y1'
                                   )
                        )

    return trace_pol_th






