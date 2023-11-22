import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import ode

def HH_old(i_inj, time_tot, rest_potential=0):
    # constants
    g_k = 36      # [mS/cm^2]
    g_Na = 120    # [mS/cm^2]
    g_l = 0.3     # [mS/cm^2]
    E_k = rest_potential - 12      # [mV]
    E_Na = rest_potential + 115    # [mV]
    E_l = rest_potential + 10.613  # [mV]
    Cm = 1                         # [microF/cm^2]

    #  determine the percent (from the total time) that there is a step current
    step_start_percent = 15
    step_stop_percent = 30

    DeltaT = 0.01                           # using Euler Method
    samples = math.ceil(time_tot/DeltaT)    # [mS] ,an integer. will be useful to init the variables

    # init variables
    time = np.arange(0, samples) * DeltaT   # the time axis of the simulation
    V = np.zeros(samples)                   # the voltage of neuron
    M = np.zeros(samples)                   # activation variable for Na current
    H = np.zeros(samples)                   # inactivation variable for Na current
    N = np.zeros(samples)                   # activation variable for K current

    current_inj = np.zeros(samples)
    np.put(current_inj, np.arange(samples * (step_start_percent / 100),
                                  samples * (step_stop_percent / 100), 1, dtype=int), i_inj)

    V[0] = rest_potential
    M[0] = alphaM(V[0])/(alphaM(V[0]) + betaM(V[0]))
    H[0] = alphaH(V[0])/(alphaH(V[0]) + betaH(V[0]))
    N[0] = alphaN(V[0])/(alphaN(V[0]) + betaN(V[0]))
    '''M[0] = 0.05
    H[0] = 0.6
    N[0] = 0.32'''

    # according to Euler Method we update the variables
    for i in range(0, samples - 1):
        I_tot = g_k * (N[i]**4) * (E_k-V[i]) + g_Na * (M[i]**3) * H[i] * (E_Na-V[i]) + g_l * (E_l-V[i]) + current_inj[i]
        V[i+1] = V[i] + DeltaT*I_tot/Cm

        # now we can place the voltage in the equations of the variables
        M[i+1] = M[i] + DeltaT*(alphaM(V[i])*(1-M[i]) - betaM(V[i])*M[i])
        H[i+1] = H[i] + DeltaT*(alphaH(V[i])*(1-H[i]) - betaH(V[i])*H[i])
        N[i+1] = N[i] + DeltaT*(alphaN(V[i])*(1-N[i]) - betaN(V[i])*N[i])

    return V, M, H, N, time


def HH(i_inj, time_tot, rest_potential=-70):

    # constants
    g_k = 36  # [mS/cm^2]
    g_Na = 120  # [mS/cm^2]
    g_l = 0.3  # [mS/cm^2]
    E_k = rest_potential - 12  # [mV]
    E_Na = rest_potential + 115  # [mV]
    E_l = rest_potential + 10.613  # [mV]
    Cm = 1  # [microF/cm^2]

    E_k = - 12  # [mV]
    E_Na = 115  # [mV]
    E_l = 10.613  # [mV]

    #  determine the percent (from the total time) that there is a step current
    step_start_percent = 15
    step_stop_percent = 30

    DeltaT = 0.01  # using Euler Method
    samples = math.ceil(time_tot / DeltaT)  # [mS] ,an integer. will be useful to init the variables

    # init variables
    time = np.arange(0, samples) * DeltaT  # the time axis of the simulation
    V = np.zeros(samples)  # the voltage of neuron
    M = np.zeros(samples)  # activation variable for Na current
    H = np.zeros(samples)  # inactivation variable for Na current
    N = np.zeros(samples)  # activation variable for K current

    current_inj = np.zeros(samples)
    np.put(current_inj, np.arange(samples * (step_start_percent / 100),
                                  samples * (step_stop_percent / 100), 1, dtype=int), i_inj)

    V[0] = rest_potential
    M[0] = alphaM(V[0]) / (alphaM(V[0]) + betaM(V[0]))
    H[0] = alphaH(V[0]) / (alphaH(V[0]) + betaH(V[0]))
    N[0] = alphaN(V[0]) / (alphaN(V[0]) + betaN(V[0]))

    M[0] = 0
    H[0] = 1
    N[0] = 0

    # Create an ODE solver using 4th-order Runge-Kutta
    solver = ode(model_derivatives)
    solver.set_initial_value([V[0], M[0], H[0], N[0]], 0)

    # Simulate the HH model
    for i in range(1, samples):
        solver.set_f_params(current_inj[i], Cm, g_k, E_k, g_Na, E_Na, g_l, E_l)
        solver.integrate(solver.t + DeltaT)
        V[i], M[i], H[i], N[i] = solver.y

    return V, M, H, N, time


def model_derivatives(t, y, i_inj, Cm, g_k, E_k, g_Na, E_Na, g_l, E_l):
    V, M, H, N = y
    # Calculate derivatives for the gating variables and V based on the HH equations
    dVdt = (1 / Cm) * (i_inj - g_k * (N**4) * (V - E_k) - g_Na * (M**3) * H * (V - E_Na) - g_l * (V - E_l))
    dMdt = alphaM(V) * (1 - M) - betaM(V) * M
    dHdt = alphaH(V) * (1 - H) - betaH(V) * H
    dNdt = alphaN(V) * (1 - N) - betaN(V) * N
    return [dVdt, dMdt, dHdt, dNdt]


# alpha & beta functions
def alphaN(v):
    return (10 - v)/(100*(np.exp((10 - v)/10) - 1))


def betaN(v):
    return 0.125*np.exp((-v)/80)


def alphaM(v):
    return (25 - v)/(10*(np.exp((25 - v)/10)-1))


def betaM(v):
    return 4*np.exp(-v/18)


def alphaH(v):
    return 0.07*np.exp(-v/20)


def betaH(v):
    return 1/(1+np.exp((30-v)/10))


# ass 1, action potential and dynamics of the gates


def plot_potential(i_inj, time_tot):
    [V, M, H, N, time] = HH(i_inj, time_tot)
    # V = V - 70
    f = plt.figure(1, figsize=(5, 3.5))
    plt.plot(time, V)
    plt.title('Action potential voltage')
    plt.legend('V [mV]')
    plt.xlabel('Time [msec]')
    plt.ylabel('Voltage [mV]')
    return f


def plot_dynamics(i_inj, time_tot):
    [V, M, H, N, time] = HH(i_inj, time_tot)
    f = plt.figure(2, figsize=(5, 2.5))
    plt.plot(time, M, time, H, 'r-', time, N, 'g-')
    plt.title('Dynamics of the 3 gating particles')
    plt.legend(['M', 'H', 'N'], loc='upper right')
    plt.xlabel('Time [msec]')
    plt.ylabel('Probability for a gate to open')
    return f


# i_inj = 15
# time_tot = 30
# plot_potential(i_inj, time_tot)
# plot_dynamics(i_inj, time_tot)
