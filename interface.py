import tkinter as tk

#main user interface for the simulation
class simulationWindow(tk.Frame):

    #sets up the window
    def __init__(self, parent):
        #set up the frame
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        #configure the window and make the widgets
        self.configure_gui()
        self.create_widgets()

        #state variables read from the simulation thread
        self.simulation_running = False
        self.simulation_loaded = False

    #configures the window for use
    def configure_gui(self):
        #window properties
        self.parent.geometry("350x145")
        self.parent.resizable(False, False)
        
        #configure the close protocol
        self.parent.protocol("WM_DELETE_WINDOW", self.close_window)

    #fills the frame with the required widgets
    def create_widgets(self):
        self.load_unload_bttn = tk.Button(
            self.parent,
            text="Load simulation",
            command=self.toggle_load_sim
        ) 
        self.save_sim_bttn = tk.Button(
            self.parent,
            text="Save simulation",
            command=self.save_sim
        ) 
        self.start_stop_bttn = tk.Button(
            self.parent, 
            text="Start simulation", 
            command=self.toggle_run_sim
        )
        self.create_sim_bttn = tk.Button(
            self.parent,
            text="Create new simulation",
            command=self.create_sim
        ) 

        self.load_unload_bttn.place(x=5, y=5, width=125, height=30)
        self.save_sim_bttn.place(x=5, y=40, width=125, height=30)
        self.start_stop_bttn.place(x=5, y=75, width=125, height=30)
        self.create_sim_bttn.place(x=5, y=110, width=125, height=30)

    #called when the window is to be closed
    def close_window(self):
        self.parent.destroy()

    #loads or unloads a simulation, depending on if a simulation is already loaded
    def toggle_load_sim(self):
        if self.simulation_loaded:
            print("Unloading simulation...")
            self.load_unload_bttn.config(text="Load simulation")

            self.simulation_loaded = False
        else:
            print("Loading simulation...")
            self.load_unload_bttn.config(text="Unload simulation")

            self.simulation_loaded = True

    #saves the currently loaded simulation
    def save_sim(self):
        print("Saving simulation...")

    #switches the simulation from on/off to off/on respectively
    def toggle_run_sim(self):
        if self.simulation_running:
            print("Pausing simulation...")
            self.start_stop_bttn.config(text="Start simulation")

            self.simulation_running = False
        else:
            print("Starting simulation...")
            self.start_stop_bttn.config(text="Pause simulation")

            self.simulation_running = True

    #calls the simulation class' make_dir method
    def create_sim(self):
        print("Making new sim...")

if __name__ == "__main__":
    root = tk.Tk()
    window = simulationWindow(root)
    root.mainloop()