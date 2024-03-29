import tkinter as tk
from HH_front import HHSimulatorGUI

def main():
    # Create the main window (root) for the application and set the initial size of the window
    root = tk.Tk()
    # root.geometry('1400x850+0+0')

    # Set the window to full screen
    root.state("zoomed")

    # Create an instance of the HHSimulatorGUI
    app = HHSimulatorGUI(root)

    # Set the title of the window
    root.title("Hodgkin Huxley model simulator")

    # Start the GUI event loop
    root.mainloop()

if __name__ == "__main__":
    main()