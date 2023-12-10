import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import HH_back as HH


class HHSimulatorGUI:
    def __init__(self, master):
        self.master = master

        self.neuron_status_label = tk.Label(self.master, text='', font=('Arial', 15))
        self.legend_txt = []

        # create the widgets of the GUI window
        self.create_widgets()


    def create_widgets(self):
        """Creates the widgets, titles and buttons of the window"""

        # Labels
        self.main_title = tk.Label(self.master, text="Parameters:", font=('Arial', 12))
        self.main_title.grid(row=0, column=0, pady=10)

        self.amp_title = tk.Label(self.master, text='Current step amplitude [nano Amper]')
        self.amp_title.grid(row=1, column=0, pady=10)

        self.time_title = tk.Label(self.master, text='Experiment duration [milli second]')
        self.time_title.grid(row=2, column=0, pady=10)

        # Entry text-boxs
        self.amp_spinbox = tk.Spinbox(self.master, from_=1, to=100, increment=5, width=5)
        self.amp_spinbox.grid(row=1, column=1, pady=10)
        self.amp_spinbox.delete(0, tk.END)
        self.amp_spinbox.insert(0, 15)

        self.time_spinbox = tk.Spinbox(self.master, from_=1, to=100, increment=5, width=5)
        self.time_spinbox.grid(row=2, column=1, pady=10)
        self.time_spinbox.delete(0, tk.END)
        self.time_spinbox.insert(0, 15)

        # Buttons
        self.button_plot = tk.Button(self.master, text="Plot data", command=lambda:
                                      self.plot_data(int(self.amp_spinbox.get()),
                                                      int(self.time_spinbox.get()), self.legend_txt))
        self.button_plot.grid(row=5, column=4, sticky='SE', pady=10, padx=5)

        self.button_delete = tk.Button(self.master, text="Erase data", command=self.erase_data)
        self.button_delete.grid(row=5, column=5, sticky='SE', pady=10, padx=5)


    def plot_data(self, i_inj, time_tot, legend_txt):
        """Plots the graphs in the window with the inserted entries"""

        [action_fig, self.legend_txt] = HH.plot_potential(i_inj, time_tot, legend_txt)
        dynamics_fig = HH.plot_dynamics(i_inj, time_tot)

        action_potential = FigureCanvasTkAgg(action_fig, master=self.master)
        action_potential.draw()
        action_potential.get_tk_widget().grid(row=3, column=3, pady=10)

        dynamics_plot = FigureCanvasTkAgg(dynamics_fig, master=self.master)
        dynamics_plot.draw()
        dynamics_plot.get_tk_widget().grid(row=4, column=3, pady=10)

        # Check if an action potential occurred or not and writes a message accordingly
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
        """Clears the data from the graphs in the window"""
        action_fig, dynamics_fig = self.plot_data(15, 15, self.legend_txt)
        action_fig.clear()
        dynamics_fig.clear()
        self.legend_txt = []
        self.neuron_status_label.config(text='Both graphs were erased :)')
        print('Plots erased')


if __name__ == "__main__":
    root = tk.Tk()
    app = HHSimulatorGUI(root)
    root.mainloop()
