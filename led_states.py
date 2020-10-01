import States from states
import Pin from machine

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
        print('OFF')
        return


    def red(self,last_state, state):
        print('RED')
        return


    def orange(self,last_state, state):
        print('ORANGE')
       return


    def green(self,last_state, state):
        print('GREEN')
        return
    
