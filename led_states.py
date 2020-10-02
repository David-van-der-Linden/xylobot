import States from states
import Pin from machine
import random

def LedStates:
    def __init__(self):
        self.leds = {
            "red": Pin('B0', Pin.OUT), 
            "orange": Pin('E1', Pin.OUT), 
            "green": Pin('B14', Pin.OUT)
            }

        return
    
    #not sure about values() and value()
    def all_off(self):
        for pin in self.leds.values():
            pin.value(0)
        return
    
    def toggle_led(self, key):
        if self.leds[key].value():
                self.leds[key].value(0)
                else:
                    self.leds[key].value(1)
        return

    def off(self,last_state, state):
        # Entry action
        if last_state is not state:
            self.all_off()
            last_state = state

        # Action: None
        # State guards: None. Must be done through button press
        return last_state, state


    def red(self,last_state, state):
        # Entry action
       if last_state is not state:
            self.all_off()
            last_state = state
            
        
        # Action: toggle. Leads to blink in same state
        self.toggle_led('red')

        # State guards (random)
        if random.getrandbits(1):
            state = States.ORANGE
        return last_state, state


    def green(self,last_state, state):
        # Entry action
        if last_state is not state:
            self.all_off()
            last_state = state
            
        
        # Action: toggle. Leads to blink in same state
        self.toggle_led('green')

        # State guards (random)
        if random.getrandbits(1):
            state = States.RED
       return last_state, state


    def orange(self,last_state, state):
       # Entry action
        if last_state is not state:
            self.all_off()
            last_state = state
            
         
        # Action: toggle. Leads to blink in same state
        self.toggle_led('orange')

        # State guards (random)
        if random.getrandbits(1):
            state = States.GREEN
        return last_state, state
    
