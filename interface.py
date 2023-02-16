import tkinter as tk
import tkinter.filedialog as tkfd

#main user interface for the simulation
class SimulationWindow(tk.Frame):

    #sets up the window
    def __init__(self, sim_class, parent):
        #set up the frame
        self.parent = parent
        tk.Frame.__init__(self, self.parent)

        #store simulation class and initialise variables
        self.sim_class = sim_class
        self.sim_instance = None

        #configure the window and make the widgets
        self.configure_gui()
        self.create_widgets()

        #state variables read from the simulation thread
        self.simulation_running = False
        self.simulation_loaded = False

    #configures the window for use
    def configure_gui(self):
        #window properties
        self.parent.geometry("450x145")
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

        self.active_sim_lbl = tk.Label(text="Active simulation: None", anchor="nw", wraplength=240)

        self.load_unload_bttn.place(x=5, y=5, width=125, height=30)
        self.save_sim_bttn.place(x=5, y=40, width=125, height=30)
        self.start_stop_bttn.place(x=5, y=75, width=125, height=30)
        self.create_sim_bttn.place(x=5, y=110, width=125, height=30)
        self.active_sim_lbl.place(x=140, y=5, width=250, height=100)

    #called when the window is to be closed
    def close_window(self):
        #stop and save the simulation before exiting
        if not self.sim_instance is None:
            self.sim_instance.stop()
            self.sim_instance.save()

        self.parent.destroy()

    #loads or unloads a simulation, depending on if a simulation is already loaded
    def toggle_load_sim(self):
        if self.simulation_loaded:
            print("Unloading simulation...")
            self.load_unload_bttn.config(text="Load simulation")

            #stop the simulation, save, and destroy the instance
            self.sim_instance.stop()
            self.sim_instance.save()
            self.sim_instance = None

            #reset the buttons
            self.simulation_running = False
            self.start_stop_bttn.config(text="Start simulation")
            self.active_sim_lbl.config(text="Active simulation: None")

            self.simulation_loaded = False
        else:
            #get a path and create the instance
            path = tkfd.askdirectory()

            #exit if empty path (no directory selected)
            if path == "":
                return

            #only proceed if instance creation was successful
            self.sim_instance = self.sim_class.load_sim(path)
            if not self.sim_instance is None:
                print("Loading simulation...")
                self.load_unload_bttn.config(text="Unload simulation")

                self.simulation_loaded = True
                self.active_sim_lbl.config(text=f"Active simulation: {path}")

    #saves the currently loaded simulation
    def save_sim(self):
        #guard clause: exit if we don't have a sim instance
        if self.sim_instance is None:
            return

        print("Saving simulation...")
        #stop the simulation, save, and restart
        was_paused = self.sim_instance.sim_paused
        was_active = self.sim_instance.has_started()

        self.sim_instance.stop()
        self.sim_instance.save()

        #start the simulation if it was already started before saving
        if was_active:
            self.sim_instance.start()

        #pause the simulation if it was already paused before saving
        if was_paused:
            self.sim_instance.pause()

    #switches the simulation from on/off to off/on respectively
    def toggle_run_sim(self):
        #guard clause: exit if we don't have a sim instance
        if self.sim_instance is None:
            return

        if self.simulation_running:
            print("Pausing simulation...")
            self.start_stop_bttn.config(text="Unpause simulation")

            self.sim_instance.pause()

            self.simulation_running = False
        else:
            print("Starting simulation...")
            self.start_stop_bttn.config(text="Pause simulation")

            #only unpause if there's a thread already. otherwise, start one
            if self.sim_instance.has_started():
                self.sim_instance.unpause()
            else:
                self.sim_instance.start()

            self.simulation_running = True

    #calls the simulation class' make_dir method
    def create_sim(self):
        #get simulation directory to open
        path = tkfd.askdirectory()

        #pass to simulation class
        self.sim_class.create_new_sim(path + "/New Simulation")

if __name__ == "__main__":
    from simulation import Simulation
    import pathlib
    import time
    import json

    #console colours
    import os
    os.system("")

    class TestSim(Simulation):
        def __init__(self, path, **kwargs):
            Simulation.__init__(self, path, **kwargs)

            self.tick = self.manifest["Simulation update"]

            print(kwargs, sep="\n")

        def save(self):
            #update the manifest
            self.manifest["Simulation update"] = self.tick

            #call the parent class' save method to save the manifest
            Simulation.save(self)

        @staticmethod
        def configure_new_sim(path):
            #create the manifest
            manifest = {
                "Genomes Directory" : "Genomes",
                "Networks Directory" : "Networks",
                "Genomes" : [],
                "Networks" : [],
                "Simulation update" : 0
            }
            with open(path + "/manifest.json", "w", encoding="utf-8") as f:
                json.dump(manifest, f)

            #create the directories
            pathlib.Path(path + "/Genomes").mkdir()
            pathlib.Path(path + "/Networks").mkdir()

        #thread target for the simulation thread
        def sim_thread_target(self):
            self.sim_stopped = False

            #simulation setup goes here
            Simulation.log("Initialising simulation...")

            #update loop
            while self.sim_running:
                self.sim_active = True
                
                #each simulation tick goes here
                time.sleep(0.25)
                self.tick += 1
                Simulation.log(f"Tick {self.tick}: Doing cool simulation stuff... ")

                #wait until the simulation is unpaused before doing the next tick
                while self.sim_paused and self.sim_running:
                    self.sim_active = False
                    time.sleep(0.1)

            #simulation cleanup goes here
            Simulation.log("Simulation closing...")
            self.sim_stopped = True


    root = tk.Tk()
    window = SimulationWindow(TestSim, root)
    root.mainloop()