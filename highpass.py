
class Highpassfirstorder():

    def __init__(self, sampling_frequency, static_gain, cutoff_frequency):
        
        self.sampling_frequency = sampling_frequency
        self.a = static_gain  # Absolut value of the Transferfunction of the Filter for f-->infinity
        self.cutoff_frequency = cutoff_frequency

        self.inputvalues = [0, 0]  # Has on position 0 value x[n], 1->x[n-1]

        self.outputvalues = [0, 0]  # Has on position 0 value y[n], 1->y[n-1]
        self.frequency_constant = 0.5 / self.sampling_frequency * self.cutoff_frequency
        return

    def usehighpass(self, currentvalue):
        # put new Value in the input array
       
        self.inputvalues[1] = self.inputvalues[0]
        self.inputvalues[0] = currentvalue

        # rearrange output value array
        self.outputvalues[1] = self.outputvalues[0]
        # calculate new output value
        self.outputvalues[0] = ((self.a * self.inputvalues[0] - self.a * self.inputvalues[1]) /
                                (1 + self.frequency_constant)) - self.outputvalues[1] * (self.frequency_constant - 1)
        
        return self.outputvalues[0]
