"""

"""

import numpy as np


class Neuron:
    #class variables. mostly just settings related to global neuron function
    #the thought behind this is that if these values need to be changed depending on
    #where this code is used, they can just be changed globally for all neurons without
    #each neuron having a copy, *and* avoiding global variables

    #TODO base these off of literature. default values should assume 1ms/timestep (SUBJECT TO CHANGE, 
    #ALSO BASED ON LITERATURE. PROVIDE SOURCES!)

    #the value that excitation must surpass for a spike to occur
    spike_threshold = 100
    #the value that charge is set to when a spike occurs
    spike_charge = 5

    #the value that refractory_state is set to when a spike occurs
    refractory_period = 30

    #the factor by which excitation decays by each timestep. irrespective of any other factor. multiplicative
    excitation_decay = 0.99
    #the amount that refractory_state decays by each timestep. irrespective of any other factors. additive
    refractory_decay = 1
    #the amount that charge decays by each timestep. irrespective of any other factors. additive
    charge_decay = 1

    def __init__(self):
        #initialise the neuron's internal state
        self.excitation = 0
        self.charge = 0
        self.refractory_state = 0

    #TODO: explain what each of these variables represent

    #performs one timestep for this neuron
    #swi: the sum of the neuron's weighted inputs
    def step(self, swi):
        #update excitation
        self.excitation *= Neuron.excitation_decay
        self.excitation += swi

        #update charge state
        if self.charge > 0:
            #apply charge decay, but ensure charge never drops below zero
            self.charge = max(self.charge - Neuron.charge_decay, 0)
            
        #update refractory state
        if self.refractory_state > 0:
            #apply refractory state decay, but ensure refractory_state never drops below zero
            self.refractory_state = max(self.refractory_state - Neuron.refractory_decay, 0)

        #check for spike threshold
        if self.excitation > Neuron.spike_threshold:
            #only spike if we're not in a refractory state
            if self.refractory_state == 0:
                #start a spike, reset excitation and enter a refractory state
                self.charge = Neuron.spike_charge
                self.excitation = 0
                self.refractory_state = Neuron.refractory_period


        return self.output()

    #TODO: neurotransmitter concentration
    #TODO: neurotransmitter concentration should be decreased proportional to the output strength
    #returns the output state of the neuron at the current internal state
    def output(self):
        return 1 if self.charge > 0 else 0

    #returns a string representation of the neuron's internal state
    def __str__(self):
        return f"{self.excitation:.3f}, {self.charge:.3f}, {self.refractory_state:.3f}"

if __name__ == "__main__":
    import time
    import random

    #test settings
    n_ticks = 500
    tick_delay_ms = 60


    #create a neuron, and provide it with constant input for n_ticks iterations
    neuron = Neuron()

    for t in range(n_ticks):
        input = 8 * random.random()
        print(neuron.step(input), neuron, input)
        time.sleep(tick_delay_ms / 1000)