## Hodgkin-Huxley Model

This project provides an interactive tool for exploring the behavior of a neuron using the Hodgkin-Huxley model. It is designed for students in Ben Gurion University's Intro to Computational Neuroscience course taught by Dr. Tal Golan.

### Files:

- **HH_back.py**: This file defines the Hodgkin-Huxley Model function, which simulates the neuron's electrical activity, and some other functions. 
It includes the following functions:
  - `HH` function that simulates the Hodgkin-Huxley Model and returns 5 vectors: voltage, gatings M, H and N and time.
  - Supporing `alpha` and `beta` functions (for each gate N, M and H) that calculates the the values of the gates probability.
  - `plot_potential` function that plots a graph of voltage as a function of time and returns it's figure.
  - `plot_dynamics` function that plots the dynamics of the gates N, M and H as a function of time and returns it's figure.
  - `is_action_potential` function that checks if the voltage surpass a threshold to determine if the neuron fired.
- **HH_front.py**: This file defines the `HHSimulatorGUI` class, which provides a visualization of the neuron's membrane potential and the gates dynamics. 
It includes the following methods:
  - `__init__` to create the main window
  - `create_widgets` to create all of the labels and buttons
  - `plot_data` to display the plots of the voltage and the gates opening probability from the backend.
  - `erase_data` to erase the old plots of the voltage and the gates opening probability.
- **main.py**: This file defines the `main` function which starts the application and calls for the front window.

### Execution:

1. Make sure you have Python 3.x and the necessary libraries installed (details in the dependencies section).
2. Open a terminal window and navigate to the project directory.
3. Run the following command to start the GUI:

```
python main.py
```

4. The GUI will appear, allowing you to:
   - Adjust the neuron model parameters using the sliders.
   - Observe the membrane potential and the gates opening probabilities through the graphs.
   - Plot and erase the graphs.

### Dependencies and Prerequisites:

- Python 3.x
- Numpy
- Math
- Matplotlib
- Tkinter

### Theoretical Description:

The Hodgkin-Huxley model is a mathematical model that describes how action potentials in neurons are initiated and propagated. It is a set of nonlinear differential equations that approximates the electrical engineering characteristics of excitable cells such as neurons and muscle cells. It is a continuous-time dynamical system.

### Customizable Variables:

The GUI allows you to modify the following parameters of the integrate-and-fire model:

- **Step current amplitude**: The amplitude of the step current thats injected to the neuron.
- **Experiment duration**: The amount of time the model is active.

By adjusting these parameters, you can explore how they influence the neuron's firing behavior and gain a deeper understanding of the Hodgkin-Huxley model.

## Interactive Platform:

This project serves as an interactive platform for students to:

- **Visualize**: Observe the dynamic behavior of the Hodgkin-Huxley model.
- **Experiment**: Actively manipulate and explore the impact of various parameters on neuronal activity.
- **Program**: Gain practical hands-on experience with Python programming by tweaking the code itself and directly observing the resulting changes in the model's behavior.

We encourage you to actively engage with this project by experimenting, exploring, and modifying the code to solidify your knowledge and gain a deeper appreciation for the fascinating world of computational neuroscience!

---

Developed by Yuval Partok.
