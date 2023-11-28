import tkinter as tk
from HH_front import HHSimulatorGUI
import HH_front

def main():
    # Create the main window (root) for the application and set the initial size of the window
    root = tk.Tk()
    root.geometry('1100x850+0+0')

    # Create an instance of the HHSimulatorGUI
    app = HHSimulatorGUI(root)

    # Set the title of the window
    root.title("Hodgkin Huxley model simulator")

    # Start the GUI event loop
    root.mainloop()


if __name__ == "__main__":
    main()