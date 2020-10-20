

class Rmsfilter():

    
    def __init__(self,window_size):
        self.window_size=window_size 
        self.values=[]
        self.squaredsum = 0
        return
    
    def process(self,new_value):
        self.values.append(new_value)
        self.squaredsum += new_value
        if len(self.values)> self.window_size:
            self.squaredsum -= (self.values.pop(0))
            #self.values.pop()

        return abs(self.squaredsum/len(self.values))



