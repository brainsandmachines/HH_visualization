import tkinter as tk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

import HH_back as HH


class HHSimulatorGUI:
    def __init__(self, master):
        self.master = master
        self.create_main_frames()

        self.neuron_state_label = tk.Label(self.status_frame, text='', font=('Arial', 15))
        self.legend_txt = []

        self.action_fig = None
        self.dynamics_fig = None
        self.step_current_fig = None

        self.action_potential = None
        self.dynamics_plot = None
        self.step_current = None
        
        self.stack_plots = tk.IntVar()
        self.plotted = False

        self.N_active = tk.BooleanVar(value=True)
        self.M_active = tk.BooleanVar(value=True)
        self.H_active = tk.BooleanVar(value=True)

        # create the widgets of the GUI window
        self.create_widgets()


    def create_main_frames(self):
        """Creates the main frames for the widgets"""
        self.control_frame = tk.Frame(self.master)
        self.control_frame.grid(row=1, column=0, sticky='NW', pady=5, padx=5)

        self.buttons_frame = tk.Frame(self.control_frame)
        self.buttons_frame.grid(row=2, column=0, sticky='SW', pady=5, padx=5)

        self.status_frame = tk.Frame(self.control_frame)
        self.status_frame.grid(row=3, column=0, sticky='SW', pady=5, padx=5)


    def create_widgets(self):
        """Creates the widgets, titles and buttons of the window"""
        # Labels
        self.main_title = tk.Label(self.master, text="Parameters:", font=('Arial', 12))
        self.main_title.grid(row=0, column=0, pady=10)

        self.amp_title = tk.Label(self.control_frame, text='Current step amplitude [nano Amper]')
        self.amp_title.grid(row=0, column=0, pady=10)

        self.time_title = tk.Label(self.control_frame, text='Experiment duration [milli second]')
        self.time_title.grid(row=1, column=0, pady=10)

        self.neuron_status_headline = tk.Label(self.status_frame, text='Neuron status:', font=('Arial', 15))
        self.neuron_status_headline.grid(row=0, column=0, pady=10, padx=10)

        # Entry text-boxs
        self.amp_spinbox = tk.Spinbox(self.control_frame, from_=1, to=100, increment=5, width=5)
        self.amp_spinbox.grid(row=0, column=1, pady=10)
        self.amp_spinbox.delete(0, tk.END)
        self.amp_spinbox.insert(0, 15)

        self.time_spinbox = tk.Spinbox(self.control_frame, from_=1, to=100, increment=5, width=5)
        self.time_spinbox.grid(row=1, column=1, pady=10)
        self.time_spinbox.delete(0, tk.END)
        self.time_spinbox.insert(0, 15)

        # Buttons
        self.button_plot = tk.Button(self.buttons_frame, text="Plot data", command=lambda:
                                      self.plot_data(float(self.amp_spinbox.get()),
                                                      int(self.time_spinbox.get())))
        self.button_plot.grid(row=0, column=0, sticky='SW', pady=10, padx=5)

        self.button_delete = tk.Button(self.buttons_frame, text="Erase data", command=self.erase_data)
        self.button_delete.grid(row=0, column=1, sticky='SW', pady=10, padx=5)

        # Checkboxes
        self.stack_checkbox = tk.Checkbutton(self.buttons_frame, text='Stack plots',
                                              variable=self.stack_plots, onvalue=1, offvalue=0)
        self.stack_checkbox.grid(row=0, column=2, sticky='SW', pady=10, padx=5)

        self.N_active_checkbox = tk.Checkbutton(self.buttons_frame, text='Deactivate N',
                                                 variable=self.N_active, onvalue=False, offvalue=True)
        self.N_active_checkbox.grid(row=1, column=0, sticky='SW', pady=5, padx=5)
        
        self.M_active_checkbox = tk.Checkbutton(self.buttons_frame, text='Deactivate M',
                                                 variable=self.M_active, onvalue=False, offvalue=True)
        self.M_active_checkbox.grid(row=1, column=1, sticky='SW', pady=5, padx=5)
        
        self.H_active_checkbox = tk.Checkbutton(self.buttons_frame, text='Deactivate H',
                                                 variable=self.H_active, onvalue=False, offvalue=True)
        self.H_active_checkbox.grid(row=1, column=2, sticky='SW', pady=5, padx=5)


    def plot_data(self, i_inj, time_tot):
        """Plots the graphs in the window with the inserted entries"""
        if self.stack_plots.get() == 0:
            if self.plotted:
                self.erase_data()

        N_active = self.N_active.get()
        M_active = self.M_active.get()
        H_active = self.H_active.get()

        self.create_legend_txt(i_inj, time_tot)

        self.action_fig = HH.plot_potential(i_inj, time_tot, N_active, M_active,
                                                                H_active, self.legend_txt)
        self.dynamics_fig = HH.plot_dynamics(i_inj, time_tot, N_active, M_active, H_active)
        self.step_current_fig = HH.plot_step_current(i_inj, time_tot, self.legend_txt)

        self.action_potential = FigureCanvasTkAgg(self.action_fig, master=self.master)
        self.action_potential.draw()
        self.action_potential.get_tk_widget().grid(row=1, column=1, pady=2)

        self.dynamics_plot = FigureCanvasTkAgg(self.dynamics_fig, master=self.master)
        self.dynamics_plot.draw()
        self.dynamics_plot.get_tk_widget().grid(row=2, column=1, pady=2)

        self.step_current = FigureCanvasTkAgg(self.step_current_fig, master=self.master)
        self.step_current.draw()
        self.step_current.get_tk_widget().grid(row=1, column=2, pady=2, padx=2)

        # Check if an action potential occurred or not and writes a message accordingly
        if HH.is_action_potential(i_inj, time_tot):
            neuron_status = "Action potential occurred!"
        else:
            neuron_status = "Neuron didn't fire this time"
        
        # neuron_status_label = tk.Label(self.master, text='neuron_status', font=('Arial', 15))
        self.neuron_state_label.config(text=neuron_status)
        self.neuron_state_label.grid(row=1, column=0, pady=10, padx=10)

        self.plotted = True


    def erase_data(self):
        """Clears the data from the graphs in the window"""
        self.action_fig = self.action_fig.clf()
        self.dynamics_fig = self.dynamics_fig.clf()
        self.step_current_fig = self.step_current_fig.clf()
        self.legend_txt = []

        self.action_potential.draw()
        self.dynamics_plot.draw()
        self.step_current.draw()

        self.plotted = False

        self.neuron_state_label.config(text='Both graphs were erased')


    def create_legend_txt(self, i_inj, time_tot):
        new_legend = str(i_inj) + '[nA], ' + str(time_tot) + '[msec]'
        self.legend_txt.append(new_legend)



if __name__ == "__main__":
    root = tk.Tk()
    app = HHSimulatorGUI(root)
    root.mainloop()
