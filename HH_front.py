import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import HH_back as HH


class HHSimulatorGUI:
    def __init__(self, master):
        self.master = master

        self.neuron_state_label = tk.Label(self.master, text='', font=('Arial', 15))
        self.legend_txt = []
        self.action_fig = None
        self.dynamics_fig = None

        self.action_potential = None
        self.dynamics_plot = None
        
        self.stack_plots = tk.IntVar()
        self.plotted = False

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

        self.neuron_status_headline = tk.Label(self.master, text='Neuron status:', font=('Arial', 15))
        self.neuron_status_headline.grid(row=1, column=3, pady=10, padx=10)

        # Entry text-boxs
        self.amp_spinbox = tk.Spinbox(self.master, from_=1, to=100, increment=5, width=5)
        self.amp_spinbox.grid(row=1, column=1, pady=10)
        self.amp_spinbox.delete(0, tk.END)
        self.amp_spinbox.insert(0, 15)

        self.time_spinbox = tk.Spinbox(self.master, from_=1, to=100, increment=5, width=5)
        self.time_spinbox.grid(row=2, column=1, pady=10)
        self.time_spinbox.delete(0, tk.END)
        self.time_spinbox.insert(0, 15)


        self.buttons_frame = tk.Frame(self.master)
        self.buttons_frame.grid(row=3, column=0, sticky='SW', pady=5, padx=5)

        # Buttons
        self.button_plot = tk.Button(self.buttons_frame, text="Plot data", command=lambda:
                                      self.plot_data(int(self.amp_spinbox.get()),
                                                      int(self.time_spinbox.get()), self.legend_txt))
        self.button_plot.grid(row=0, column=0, sticky='SW', pady=10, padx=5)

        self.button_delete = tk.Button(self.buttons_frame, text="Erase data", command=self.erase_data)
        self.button_delete.grid(row=0, column=1, sticky='SW', pady=10, padx=5)

        self.checkbox = tk.Checkbutton(self.buttons_frame, text='Stack plots',variable=self.stack_plots, onvalue=1, offvalue=0)
        self.checkbox.grid(row=0, column=2, sticky='SW', pady=10, padx=5)


    def plot_data(self, i_inj, time_tot, legend_txt):
        """Plots the graphs in the window with the inserted entries"""
        if self.stack_plots.get() == 0:
            if self.plotted:
                self.erase_data()

        [self.action_fig, self.legend_txt] = HH.plot_potential(i_inj, time_tot, legend_txt)
        self.dynamics_fig = HH.plot_dynamics(i_inj, time_tot)

        self.action_potential = FigureCanvasTkAgg(self.action_fig, master=self.master)
        self.action_potential.draw()
        self.action_potential.get_tk_widget().grid(row=4, column=3, pady=2)

        self.dynamics_plot = FigureCanvasTkAgg(self.dynamics_fig, master=self.master)
        self.dynamics_plot.draw()
        self.dynamics_plot.get_tk_widget().grid(row=5, column=3, pady=2)

        # Check if an action potential occurred or not and writes a message accordingly
        if HH.is_action_potential(i_inj, time_tot):
            neuron_status = "Action potential occurred!"
        else:
            neuron_status = "Neuron didn't fire this time"
        
        # neuron_status_label = tk.Label(self.master, text='neuron_status', font=('Arial', 15))
        self.neuron_state_label.config(text=neuron_status)
        self.neuron_state_label.grid(row=2, column=3, pady=10, padx=10)

        self.plotted = True


    def erase_data(self):
        """Clears the data from the graphs in the window"""
        # action_fig, dynamics_fig = self.plot_data(15, 15, self.legend_txt)
        self.action_fig = self.action_fig.clf()
        self.dynamics_fig = self.dynamics_fig.clf()
        self.legend_txt = []

        self.action_potential.draw()
        self.dynamics_plot.draw()

        self.plotted = False

        self.neuron_state_label.config(text='Both graphs were erased :)')


if __name__ == "__main__":
    root = tk.Tk()
    app = HHSimulatorGUI(root)
    root.mainloop()
