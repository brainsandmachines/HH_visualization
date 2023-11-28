import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import HH_backend as HH


class HHSimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Hodgkin Huxley model simulator")

        self.neuron_status_label = tk.Label(self.master, text='', font=('Arial', 15))

        # create the widgets of the GUI window
        self.create_widgets()


    def create_widgets(self):
        # Labels
        self.main_title = tk.Label(self.master, text="Parameters:", font=('Arial', 12))
        self.main_title.grid(row=0, column=0, pady=10)

        self.amp_title = tk.Label(self.master, text='current step amplitude [nano Amper]')
        self.amp_title.grid(row=1, column=0, pady=10)

        self.time_title = tk.Label(self.master, text='current step duration [milli second]')
        self.time_title.grid(row=2, column=0, pady=10)

        # Entry text-boxs
        self.amp_text = tk.Entry(self.master, width=5)
        self.amp_text.grid(row=1, column=1, pady=10)
        self.amp_text.insert(0, 15)

        self.time_text = tk.Entry(self.master, width=5)
        self.time_text.grid(row=2, column=1, pady=10)
        self.time_text.insert(0, 15)

        # Buttons
        self.button_plot = tk.Button(self.master, text="Plot data", command=lambda: self.plot_data(int(self.amp_text.get()), int(self.time_text.get())))
        self.button_plot.grid(row=5, column=4, sticky='SE', pady=10, padx=5)

        self.button_delete = tk.Button(self.master, text="Erase data", command=self.erase_data)
        self.button_delete.grid(row=5, column=5, sticky='SE', pady=10, padx=5)


    def plot_data(self, i_inj, time_tot):
        action_fig = HH.plot_potential(i_inj, time_tot)
        dynamics_fig = HH.plot_dynamics(i_inj, time_tot)

        action_potential = FigureCanvasTkAgg(action_fig, master=self.master)
        action_potential.draw()
        action_potential.get_tk_widget().grid(row=3, column=3, pady=10)

        dynamics_plot = FigureCanvasTkAgg(dynamics_fig, master=self.master)
        dynamics_plot.draw()
        dynamics_plot.get_tk_widget().grid(row=4, column=3, pady=10)

        if HH.is_action_potential(i_inj, time_tot):
            neuron_status = "Action potential occurred!"
        else:
            neuron_status = "Neuron didn't fire this time"
        
        # neuron_status_label = tk.Label(self.master, text='neuron_status', font=('Arial', 15))
        self.neuron_status_label.config(text=neuron_status)
        self.neuron_status_label.grid(row=3, column=4, pady=10, padx=10)

        print('plot created')
        return action_fig, dynamics_fig


    def erase_data(self):
        action_fig, dynamics_fig = self.plot_data(15, 15)
        action_fig.clear()
        dynamics_fig.clear()
        self.neuron_status_label.config(text='Both graphs were erased :)')
        print('Plots erased')


if __name__ == "__main__":
    root = tk.Tk()
    app = HHSimulatorGUI(root)
    root.mainloop()
