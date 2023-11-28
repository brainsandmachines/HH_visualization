import numpy as np
import math
import matplotlib.pyplot as plt
from scipy.integrate import ode



def HH(i_inj, time_tot):

    # constants
    rest_potential = -70  # [mV]
    g_k = 36              # [mS/cm^2]
    g_Na = 120            # [mS/cm^2]
    g_l = 0.3             # [mS/cm^2]
    E_k = - 77            # [mV]
    E_Na = 50             # [mV]
    E_l = - 54.4          # [mV]
    Cm = 1                # [microF/cm^2]

    #  determine the percent (from the total time) that there is a step current
    step_start_percent = 15
    step_stop_percent = 30

    DeltaT = 0.001  # using Euler Method
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


# Alpha & Beta functions
def alphaN(v):
    return (0.01*(v + 55))/(1 - np.exp((-(v + 50))/10))


def betaN(v):
    return 0.125*np.exp((-(v + 65))/80)


def alphaM(v):
    return (0.1*(v + 40))/(1 - np.exp((- (v + 40))/10))


def betaM(v):
    return 4*np.exp(-(v + 65)/18)


def alphaH(v):
    return 0.07*np.exp(-(v + 65)/20)


def betaH(v):
    return 1/(1 + np.exp(-(v + 35)/10))


def plot_potential(i_inj, time_tot):
    [V, M, H, N, time] = HH(i_inj, time_tot)
    f = plt.figure(1, figsize=(5, 3.8))
    plt.plot(time, V)
    plt.title('Action potential voltage')
    plt.legend('V [mV]')
    plt.xlabel('Time [msec]')
    plt.ylabel('Voltage [mV]')
    return f


def plot_dynamics(i_inj, time_tot):
    [V, M, H, N, time] = HH(i_inj, time_tot)
    f = plt.figure(2, figsize=(5, 2.2))
    plt.plot(time, M, time, H, 'r-', time, N, 'g-')
    plt.title('Dynamics of the 3 gating particles')
    plt.legend(['M', 'H', 'N'], loc='upper right')
    plt.xlabel('Time [msec]')
    plt.ylabel('Probability for a gate to open')
    return f


def is_action_potential(i_inj, time_tot):
    [V, M, H, N, time] = HH(i_inj, time_tot)
    if V.max() >= 15:
        return True
    else:
        return False



# i_inj = 15
# time_tot = 40
# plot_potential(i_inj, time_tot)
# plot_dynamics(i_inj, time_tot)
# plt.show()
