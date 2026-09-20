from states import States
from state_object import StateObject
from state_functions import StateFunctions

from nucleo_button_control import NucleoButtonControl
from potmeter import Potmeter

# Micropython specific modules
import br_timer


class Robot(object):
    """
    Robot state machine example.
    """

    def __init__(self, timer_number, main_frequency):
        """
        =INPUT=
            timer_number - integer
                Timer number on the NUCLEO board
            main_frequency - integer
                Frequency at which the main ticker should run
        """

        self.main_frequency = main_frequency
        self.main_ticker = br_timer.ticker(
            timer_number, main_frequency, self.run, True)

        # State object instance that can be updated by other objects
        self.state_object = StateObject()

        # Objects that can update the state object
        self.nucleo_button_control = NucleoButtonControl(self.state_object)
        self.state_functions = StateFunctions(self.state_object, main_frequency)
        
        # The state machine itself
        self.state_machine = {
            States.SAFE: self.state_functions.safe,
            States.READ: self.state_functions.read,
            States.ON: self.state_functions.on
        }

        return


    def run(self):
        """
        Target for the ticker. Get's executed every time step.
        """

        # Check if the button was invoked for a state update
        self.nucleo_button_control.update_state()

        # Run the active state from the state machine
        self.state_machine[self.state_object.state]()
        return


    def start(self):
        # Ticker start
        self.main_ticker.start()
        return


    def stop(self):
        # Ticker stop
        self.main_ticker.stop()
        return

