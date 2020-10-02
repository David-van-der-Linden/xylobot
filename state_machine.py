import br_timer 
import States from states
import LedStates from led_states
from button_control import ButtonControl



def Robot:
    def __init__(self, ticker_number, main_frequency):
        self.ticker_number = ticker_number
        self.main_frequency=main_frequency
        self.main_ticker= None
        self.led_states = LedStates()
        self.last_state = None
        self.state = States.OFF
        self.button_control = ButtonControl()
        self.state_machine = {
            States.OFF: led_states.all_off,
            States.RED: led_states.red,
            States.ORANGE: led_states.orange,
            States.GREEN: led_states.green
        }
      
        
        return
    def run(self):
         self.state = self.button_control.button_state_change(self.state)
         self.last_state, self.state = self.state_machine[self.state](self.last_state, self.state)
         return 

    def start(self):
        self.main_ticker = br_timer.ticker(
            self.ticker_number,
            self.main_frequency,
            self.run,
            True
        )
        self.main_ticker.start()
        return
    
    def stop(self):
        self.main_ticker.stop()
        return
