import pathlib
import json
import threading
import time

class Simulation:
    #methods to be overriden by child classes

    #sets up the variables used for basic functionality
    def __init__(self, path, **kwargs):
        self.sim_running = True
        self.sim_paused = False
        self.sim_thread = None
        self.sim_active = False
        self.sim_stopped = True
        self.path = path
        self.manifest = kwargs
    
    #configures a newly created simulation
    @staticmethod
    def configure_new_sim(path):
        pass

    #the target function for the simulation thread
    def sim_thread_target(self):
        pass


    #parent methods that usually will not be overridden

    #saves the current state of the simulation to self.path
    def save(self):
        with open(self.path + "/manifest.json", "w", encoding="utf-8") as f:
            json.dump(self.manifest, f)

    #creates the simulation thread
    def start(self):
        #ensure that all variables are as they should be
        self.sim_running = True
        self.sim_paused = False

        #create and start the thread
        self.sim_thread = threading.Thread(target=self.sim_thread_target)
        self.sim_thread.start()

    #orders the simulation thread to stop and blocks until it does so
    def stop(self):
        self.sim_running = False
        while not self.sim_stopped:
            time.sleep(0.1)
        
        self.sim_thread = None
        self.sim_active = False

    #orders the simulation thread to pause and blocks until it does so
    def pause(self):
        self.sim_paused = True
        while self.sim_active:
            time.sleep(0.1)

    #orders the simulation thread to unpause and blocks until it does so
    def unpause(self):
        self.sim_paused = False
        while not self.sim_active:
            time.sleep(0.1)

    #returns true if the simulation has a thread
    def has_started(self):
        return not self.sim_thread is None

    #creates a new simulation of cls at path
    @classmethod
    def create_new_sim(cls, path):
        #create the directory
        pathlib.Path(path).mkdir(parents=True, exist_ok=False)

        #call the class' configure method
        cls.configure_new_sim(path)

    @classmethod
    def load_sim(cls, path):
        #verify that the path exists
        if not pathlib.Path(path).exists():
            return None

        #verify that the manifest.json exists
        if not pathlib.Path(path + "/manifest.json").exists():
            return None

        #open the manifest and pass as kwargs
        with open(path + "/manifest.json", "r", encoding="utf-8") as f:
            manifest = json.load(f)
            return cls(path, **manifest)

    #TODO add configurable logging capabilities to this
    @staticmethod
    def log(msg):
        print(f"\u001b[36m<<<SIMULATION THREAD>>>\u001b[0m {msg}")

if __name__ == "__main__":
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
                

    #create and load a sim
    try:
        TestSim.create_new_sim("Simulations/TestSim")
    except FileExistsError:
        print("Simulation already exists, continue as normal")

    sim = TestSim.load_sim("Simulations/TestSim")

    #start it, run for 5s, stop it, save it
    sim.start()
    time.sleep(5)
    sim.stop()
    sim.save()
