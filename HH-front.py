import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import HH_backend as HH

def plot_data():
    i_inj = int(amp_text.get())
    time_tot = int(time_text.get())
    action_fig = HH.plot_potential(i_inj, time_tot)
    dynamics_fig = HH.plot_dynamics(i_inj, time_tot)

    action_potential = FigureCanvasTkAgg(action_fig, master=root)
    action_potential.draw()
    action_potential.get_tk_widget().grid(row=3, column=3, pady=10)
    action_potential.get_tk_widget().grid(row=3, column=3, pady=10)

    dynamics_plot = FigureCanvasTkAgg(dynamics_fig, master=root)
    dynamics_plot.draw()
    dynamics_plot.get_tk_widget().grid(row=4, column=3, pady=10)
    # toolbar_frame_dynamic = tk.Frame(root)
    # toolbar_frame_dynamic.grid(row=2, column=0, padx=10, pady=10)
    # toolbar_dynamic = NavigationToolbar2Tk(dynamics_plot, toolbar_frame_dynamic)
    # toolbar_dynamic.update()
    dynamics_plot.get_tk_widget().grid(row=4, column=3, pady=10)
    print('plot created')
    return action_fig, dynamics_fig


def erase_data():
    action_fig, dynamics_fig = plot_data()
    action_fig.clear()
    dynamics_fig.clear()
    print('Plots erased')


# Create the main Tkinter window
root = tk.Tk()
root.title("Hodgkin-Huxley model")
root.geometry('900x850')


# Labels
main_title = tk.Label(root, text="Hello, Tkinter!")
main_title.grid(row=0, column=0, pady=10)

amp_title = tk.Label(root, text='current step amplitude [nano Amper]')
amp_title.grid(row=1, column=0, pady=10)

time_title = tk.Label(root, text='current step duration [milli second]')
time_title.grid(row=2, column=0, pady=10)


# Entry text-boxs
amp_text = tk.Entry(root, width=5)
amp_text.grid(row=1, column=1, pady=10)
amp_text.insert(0, 15)

time_text = tk.Entry(root, width=5)
time_text.grid(row=2, column=1, pady=10)
time_text.insert(0, 100)

# buttons
button_plot = tk.Button(root, text="Plot data", command=plot_data)
button_plot.grid(row=5, column=4, sticky='SE', pady=10, padx=5)

button_delete = tk.Button(root, text="Erase data", command=erase_data)
button_delete.grid(row=5, column=5, sticky='SE', pady=10, padx=5)

# Run the Tkinter event loop
root.mainloop()
