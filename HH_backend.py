import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import ode



def HH(i_inj, time_tot, rest_potential=0):

    # constants
    g_k = 36  # [mS/cm^2]
    g_Na = 120  # [mS/cm^2]
    g_l = 0.3  # [mS/cm^2]
    E_k = rest_potential - 12  # [mV]
    E_Na = rest_potential + 115  # [mV]
    E_l = rest_potential + 10.613  # [mV]
    Cm = 1  # [microF/cm^2]

    # # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # # new constants
    # g_k = 0.36  # [mS/cm^2]
    # g_Na = 1.2  # [mS/cm^2]
    # g_l = 0.003  # [mS/cm^2]
    # E_k = - 72.14  # [mV]
    # E_Na = 55.17  # [mV]
    # E_l = - 49.42  # [mV]
    # Cm = 0.01  # [microF/cm^2]

    # # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

    # E_k = - 77  # [mV]
    # E_Na = 50  # [mV]
    # E_l = - 54.402  # [mV]

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

    # according to Euler Method we update the variables
    for i in range(0, samples - 1):
        i_k = g_k*(V[i] - E_k)
        i_Na = g_Na*(V[i] - E_Na)
        i_l = g_l*(V[i] - E_l)

        dvdt = (current_inj[i] - i_Na*(M[i]**3)*H[i] - i_k*(N[i]**4) - i_l)/Cm

        V[i+1] = V[i] + dvdt*DeltaT

        # now we can place the voltage in the equations of the variables
        M[i+1] = M[i] + DeltaT*(alphaM(V[i])*(1-M[i]) - betaM(V[i])*M[i])
        H[i+1] = H[i] + DeltaT*(alphaH(V[i])*(1-H[i]) - betaH(V[i])*H[i])
        N[i+1] = N[i] + DeltaT*(alphaN(V[i])*(1-N[i]) - betaN(V[i])*N[i])

    return V, M, H, N, time

#     # Create an ODE solver using 4th-order Runge-Kutta
#     solver = ode(model_derivatives)
#     solver.set_initial_value([V[0], M[0], H[0], N[0]], 0)

#     # Simulate the HH model
#     for i in range(0, samples - 1):
#         solver.set_f_params(current_inj[i], Cm, g_k, E_k, g_Na, E_Na, g_l, E_l)
#         solver.integrate(solver.t + DeltaT)
#         V[i], M[i], H[i], N[i] = solver.y

#     return V, M, H, N, time


# def model_derivatives(t, y, i_inj, Cm, g_k, E_k, g_Na, E_Na, g_l, E_l):
#     V, M, H, N = y
#     # Calculate derivatives for the gating variables and V based on the HH equations
#     dVdt = (1 / Cm) * (i_inj - g_k * (N**4) * (V - E_k) - g_Na * (M**3) * H * (V - E_Na) - g_l * (V - E_l))
#     dMdt = alphaM(V) * (1 - M) - betaM(V) * M
#     dHdt = alphaH(V) * (1 - H) - betaH(V) * H
#     dNdt = alphaN(V) * (1 - N) - betaN(V) * N
#     return [dVdt, dMdt, dHdt, dNdt]

# M[i+1] = M[i] + DeltaT*(alphaM(V[i])*(1-M[i]) - betaM(V[i])*M[i])

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


# # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
# # new alpha & beta functions
# def alphaN(v):
#     return (0.01*(v + 50))/(1 - np.exp((-(v + 50))/10))


# def betaN(v):
#     return 0.125*np.exp((-(v + 60))/80)


# def alphaM(v):
#     return (0.1*(v + 35))/(1 - np.exp((- (v + 35))/10))


# def betaM(v):
#     return 4*np.exp(-0.0556*(v + 60))


# def alphaH(v):
#     return 0.07*np.exp(-0.05*(v + 60))


# def betaH(v):
#     return 1/(1 + np.exp(-0.1*(v + 30)))

# # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

def plot_potential(i_inj, time_tot):
    [V, M, H, N, time] = HH(i_inj, time_tot)
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


i_inj = 15
time_tot = 40
plot_potential(i_inj, time_tot)
plot_dynamics(i_inj, time_tot)
plt.show()
