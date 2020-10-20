
from highpass import Highpassfirstorder 

#creates multiple first order HighpassFilters and uses them
class Multiorderhighpass():
    """
    This class creates multiple objects of the class Highpassfirst order(depending on the Filter_order)
    These objects are stored in a list--> self.filters
    Use process() to process an input signal and run it through all of the first order filters

    """
    def __init__(self,filter_order,sample_frequecy,cutoff_frequency,static_gain):
        self.filter_order=filter_order
        self.cutoff_frequency= cutoff_frequency
        self.sample_frequecy=sample_frequecy
        self.static_gain_of_first_order_filters=static_gain 
        self.filters=[]
        #create needed amount of first order filters
        for i in range(0,filter_order):
            a = Highpassfirstorder(self.sample_frequecy,self.static_gain_of_first_order_filters,self.cutoff_frequency)
            self.filters.append(a)
        return
    
    def process(self,currentvalue):
        inputvalue = currentvalue
        for i in range(0,self.filter_order):
            inputvalue = self.filters[i].usehighpass(inputvalue)
        return inputvalue 



