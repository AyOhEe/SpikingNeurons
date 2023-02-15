"""

"""


class Neuron:
    #class variables. mostly just settings related to global neuron function
    #the thought behind this is that if these values need to be changed depending on
    #where this code is used, they can just be changed globally for all neurons without
    #each neuron having a copy, *and* avoiding global variables

    #TODO base these off of literature. default values should assume 1ms/timestep 
    #(SUBJECT TO CHANGE, ALSO BASED ON LITERATURE. PROVIDE SOURCES!)
    #TODO some factors could be provided as optional parameters in the constructor
    #(i.e. excitation_decay)

    #NOTE it looks like when this is actually being used, most coefficients will have to be
    #dialed way down, including the timestep duration. would probably need to tick these once
    #per millisecond for responsive behaviour. that isn't too bad though; it encourages
    #longer neural circuits. it'll be especially interesting to see these interact with a
    #continuous environment.

    #the value that excitation must surpass for a spike to occur
    spike_threshold = 20
    #the value that charge is set to when a spike occurs
    spike_charge = 1
    #the neurotransmitter cost coefficient while the neuron is spiking
    spike_cost_coeff = 1.5

    #TODO make refractory period proportional to the % neurotransmitters emitted (i.e a - x),
    #which should emphasise synaptic fatigue

    #the value that refractory_state is set to when a spike occurs
    refractory_period = 5

    #the baseline neurotransmitter level
    available_neurotrans = 10
    #the neurotransmitter reuptake coefficient. controls how quickly reuptake occurs. [0, 1]
    reuptake_coeff =  0.006
    #the amount of neurotransmitters required to start a spike
    neurotrans_threshold = 4

    #the factor by which excitation decays by each timestep. irrespective of any other factor. 
    #additive
    excitation_decay = 0.2
    #the amount that refractory_state decays by each timestep. irrespective of any other factors. 
    #additive
    refractory_decay = 0.5
    #the amount that charge decays by each timestep. irrespective of any other factors. additive
    charge_decay = 1

    def __init__(self):
        #initialise the neuron's internal state
        self.excitation = 0
        self.charge = 0
        self.refractory_state = 0
        self.neurotrans = Neuron.available_neurotrans

    #TODO: explain what each of these variables represent

    #performs one timestep for this neuron
    #swi: the sum of the neuron's weighted inputs
    def step(self, swi):
        #update excitation
        self.excitation -= Neuron.excitation_decay
        self.excitation += swi

        #are we spiking?
        if self.charge > 0:
            #apply neurotransmitter cost. proportional to output strength
            self.neurotrans = max(self.neurotrans - Neuron.spike_cost_coeff * self.output(), 0)
            #end the spike if we run out of neurotransmitters
            if self.neurotrans == 0:
                self.charge = 0

            #apply charge decay, but ensure charge never drops below zero
            self.charge = max(self.charge - Neuron.charge_decay, 0)

            
        #update refractory state
        if self.refractory_state > 0:
            #apply refractory state decay, but ensure refractory_state never drops below zero
            self.refractory_state = max(self.refractory_state - Neuron.refractory_decay, 0)

        #update neurotransmitters
        self.neurotrans += Neuron.reuptake_coeff * (Neuron.available_neurotrans - self.neurotrans)

        #check for spike threshold
        if self.excitation > Neuron.spike_threshold:
            #only spike if we're not in a refractory state and have enough neurotransmitters
            if self.refractory_state == 0 and self.neurotrans >= Neuron.neurotrans_threshold:
                #start a spike, reset excitation and enter a refractory state
                self.charge = Neuron.spike_charge
                self.excitation = 0
                self.refractory_state = Neuron.refractory_period



        return self.output()

    #returns the output state of the neuron at the current internal state
    def output(self):
        return 1 if self.charge > 0 else 0

    #returns a string representation of the neuron's internal state
    def __str__(self):
        txt = f"{self.excitation:.3f}, "
        txt += f"{self.charge:.3f}, "
        txt += f"{self.refractory_state:.3f}, "
        txt += f"{self.neurotrans:.3f}"

        return txt

if __name__ == "__main__":
    import random
    import matplotlib.animation as animation
    import matplotlib.pyplot as plt
    import numpy as np

    #test settings
    n_ticks = 2000
    tick_delay_ms = 20

    period = 400
    sin_offset = 0.75
    neuron_input = 4


    #TODO i'd like these graphs to be slightly prettier, with some lines showing thresholds
    #and default values on things like excitation and neurotransmitters
    
    #set up the matplot plots
    fig, axes = plt.subplots(5, 1)
    fig.set_figheight(8)
    fig.set_figwidth(15)

    axes[0].set_xlim(0, n_ticks)
    axes[0].set_ylim(0, 50)
    axes[0].set_ylabel("Excitation")
    excitation_line, = axes[0].plot([], [], lw=2)
    
    axes[1].set_xlim(0, n_ticks)
    axes[1].set_ylim(0, Neuron.spike_charge*1.1)
    axes[1].set_ylabel("Charge")
    charges_line, = axes[1].plot([], [], lw=2)
    
    axes[2].set_xlim(0, n_ticks)
    axes[2].set_ylim(0, Neuron.refractory_period*1.1)
    axes[2].set_ylabel("Refractory state")
    refractor_line, = axes[2].plot([], [], lw=2)
    
    axes[3].set_xlim(0, n_ticks)
    axes[3].set_ylim(0, Neuron.available_neurotrans*1.1)
    axes[3].set_ylabel("Neurotransmitters")
    neurotrans_line, = axes[3].plot([], [], lw=2)
    
    axes[4].set_xlim(0, n_ticks)
    axes[4].set_ylim(0, 1.1)
    axes[4].set_ylabel("Output")
    axes[4].set_xlabel("Time")
    output_line, = axes[4].plot([], [], lw=2)

    #data logging
    times = []
    excitations = []
    charges = []
    refractor_states = []
    neurotrans = []
    outputs = []

    #set up the tick function
    neuron = Neuron()

    def do_tick(t):
        #do a neuron timestep
        input = neuron_input * random.random() * max(min(np.sin(t*np.pi*2 / period)+sin_offset, 1), 0)
        print(neuron.step(input), neuron, input)

        #store the neuron's internal state and output
        times.append(t)
        excitations.append(neuron.excitation)
        charges.append(neuron.charge)
        refractor_states.append(neuron.refractory_state)
        neurotrans.append(neuron.neurotrans)
        outputs.append(neuron.output())

        #update the lines
        excitation_line.set_data(times, excitations)
        charges_line.set_data(times, charges)
        refractor_line.set_data(times, refractor_states)
        neurotrans_line.set_data(times, neurotrans)
        output_line.set_data(times, outputs)

        return excitation_line, charges_line, refractor_line, neurotrans_line, output_line,
        


    def init():
        return excitation_line, charges_line, refractor_line, neurotrans_line, output_line,

    anim = animation.FuncAnimation(fig, do_tick,
                            init_func=init,
                            frames = n_ticks,
                            interval = tick_delay_ms,
                            blit = True,
                            repeat = False)
    plt.show()
