import numpy as np
import math
import matplotlib.pyplot as plt


def HH(i_inj, time_tot, N_active=True, M_active=True, H_active=True):
    """This function emulates the Hodgkin-Huxley model and uses Euler's method for approximation. 
       input: - i_inj - the amplitude of the step current in nano Amper [nA]
              - time_tot - the total time of the expirament (only a certain precentage of the total time will
                have a step current)
       output: the function returns 5 vector of voltage, gatings M, H and N and a time vector (in that order)"""

    # Constants (rest potential, conductivity and electrochemical gradients of each ion and membrane capacitance)
    rest_potential = -70  # [mV]
    g_k = 36              # [mS/cm^2]
    g_Na = 120            # [mS/cm^2]
    g_l = 0.3             # [mS/cm^2]
    E_k = - 77            # [mV]
    E_Na = 50             # [mV]
    E_l = - 54.4          # [mV]
    Cm = 1                # [microF/cm^2]

    # Determine the percentage (from the total time) of time for the step current
    step_start_percent = 15
    step_stop_percent = 30

    # Determine the time interval and the length of the time vector
    DeltaT = 0.001
    samples = math.ceil(time_tot / DeltaT)

    # Create initial (and empty) vectors for the output
    time = np.arange(0, samples) * DeltaT  # time axis of the simulation
    V = np.zeros(samples)                  # voltage of the neuron
    M = np.zeros(samples)                  # activation variable for Na current
    H = np.zeros(samples)                  # inactivation variable for Na current
    N = np.zeros(samples)                  # activation variable for K current

    # Create the step current vector
    current_inj_vec = np.zeros(samples)
    np.put(current_inj_vec, np.arange(samples * (step_start_percent / 100),
                                  samples * (step_stop_percent / 100), 1, dtype=int), i_inj)

    # Set initial values for the vector
    V[0] = rest_potential
    M[0] = alphaM(V[0]) / (alphaM(V[0]) + betaM(V[0]))
    H[0] = alphaH(V[0]) / (alphaH(V[0]) + betaH(V[0]))
    N[0] = alphaN(V[0]) / (alphaN(V[0]) + betaN(V[0]))

    # The main for-loop that fills the output vectors
    for i in range(0, samples - 1):

        # Calculate the currents of the ions and leak current
        i_k = g_k*(V[i] - E_k)
        i_Na = g_Na*(V[i] - E_Na)
        i_l = g_l*(V[i] - E_l)

        # Checks for each of the gates if it's active. If not, it disregardes it by keeping it open
        if M_active:
            pass
        else:
            M[i] = 1

        if H_active:
            pass
        else:
            H[i] = 1

        if N_active:
            pass
        else:
            N[i] = 1

        # Calculate the new voltage value
        dvdt = (current_inj_vec[i] - i_Na*(M[i]**3)*H[i] - i_k*(N[i]**4) - i_l)/Cm
        V[i+1] = V[i] + dvdt*DeltaT

        # Now we can place the new voltage in Euler's equations of the variables
        # If one of the gates is not active, the calculation of it's new value is redundant
        M_new = M[i] + DeltaT * (alphaM(V[i]) * (1 - M[i]) - betaM(V[i]) * M[i])
        H_new = H[i] + DeltaT * (alphaH(V[i]) * (1 - H[i]) - betaH(V[i]) * H[i])
        N_new = N[i] + DeltaT * (alphaN(V[i]) * (1 - N[i]) - betaN(V[i]) * N[i])

        # Ensure the new values are within [0, 1] and update the values
        M[i+1] = min(max(M_new, 0), 1)
        H[i+1] = min(max(H_new, 0), 1)
        N[i+1] = min(max(N_new, 0), 1)

    return V, M, H, N, time, current_inj_vec


# Alpha & Beta functions that create the dynamic of the gates (N, M, H)
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



def plot_potential(i_inj, time_tot, N_active, M_active, H_active, legend_txt):
    """The function plots returns a figure with a graph of the voltage as a function of time.
       input: - i_inj - the amplitude of the step current in nano Amper [nA]
              - time_tot - the total time of the expirament (only a certain precentage of the total time will
                have a step current)
              - legend_txt - a list of the i_inj, time_tot tuples for the legend"""
    
    [V, _, _, _, time, _] = HH(i_inj, time_tot, N_active, M_active, H_active)
    f = plt.figure(1, figsize=(5, 3.8))
    plt.plot(time, V)
    plt.title('Action potential voltage')
    # new_legend = str(i_inj) + '[nA], ' + str(time_tot) + '[msec]'
    # legend_txt.append(new_legend)
    plt.legend(legend_txt, loc='upper right')
    plt.xlabel('Time [msec]')
    plt.ylabel('Voltage [mV]')
    return f


def plot_dynamics(i_inj, time_tot, N_active=True, M_active=True, H_active=True):
    """The function returns a figure with a graph of the probability of each gate's opening (in range [0,1])
       as a function of time.
       input: - i_inj - the amplitude of the step current in nano Amper [nA]
              - time_tot - the total time of the expirament (only a certain precentage of the total time will
                have a step current)"""
    
    [V, M, H, N, time, step_current] = HH(i_inj, time_tot, N_active, M_active, H_active)
    f = plt.figure(2, figsize=(5, 3.8))
    plt.plot(time, M, time, H, 'r-', time, N, 'g-')
    plt.title('Dynamics of the 3 gating particles')
    plt.legend(['M', 'H', 'N'], loc='upper right')
    plt.xlabel('Time [msec]')
    plt.ylabel('Probability for a gate to open')
    return f


def plot_dynamics_by_volt(i_inj, time_tot):
    [V, M, H, N, time, step_current] = HH(i_inj, time_tot)
    f = plt.figure(3, figsize=(5, 3.8))
    plt.plot(V, M, V, H, 'r-', V, N, 'g-')
    plt.title('Dynamics as function of voltage')
    plt.legend(['M', 'H', 'N'], loc='upper right')
    plt.xlabel('Volt [mV]')
    plt.ylabel('Probability for a gate to open')
    return f


def plot_step_current(i_inj, time_tot, legend_txt):
    [V, M, H, N, time, step_current] = HH(i_inj, time_tot)
    f = plt.figure(4, figsize=(5, 3.8))
    plt.plot(time, step_current)
    plt.title('Step current')
    # new_legend = str(i_inj) + '[nA], ' + str(time_tot) + '[msec]'
    # legend_txt.append(new_legend)
    plt.legend(legend_txt, loc='upper right')
    plt.xlabel('Time [msec]')
    plt.ylabel('Current [nA]')
    return f


def is_action_potential(i_inj, time_tot, threshold=15):
    """The function returns a boolean value thats states if an action potential has occurred
       by comparing the maximum volage to a threshold"""
    
    [V, M, H, N, time, step_current] = HH(i_inj, time_tot)
    if V.max() >= threshold:
        return True
    else:
        return False
    

i_inj = 15
time_tot = 15

# plot_step_current(i_inj, time_tot, [])
# plt.show()
plot_dynamics_by_volt(i_inj, time_tot)
plt.show()
