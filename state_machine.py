import States from states
import LedStates from led_states

import br_timer 

def Robot:
    def __init__(self, ticker_number, main_frequency):
        self.ticker_number = ticker_number
        self.main_frequency=main_frequency
        self.main_ticker= None
        self.led_states = LedStates()
        self.last_state = None
        self.state = States.RED
        self.state_machine = {
            States.OFF: led_states.all_off,
            States.RED: led_states.red,
            States.ORANGE: led_states.orange,
            States.GREEN: led_states.green
        }
     def run():
         self.last_state, self.state = self.state_machine[self.state](self.last_state, self.state)
         return   
        
        return

