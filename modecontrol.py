
import random
from states import States
import br_timer


class Modecontroler(object):

    def __init__(self, ticker_number, main_frequency):
        self.ticker_number = ticker_number
        self.main_frequency = main_frequency
        self.main_ticker = None


        self.last_state = None
        self.state = States.STATE0
        self.state_machine = {
            States.STATE0: self.state0,
            States.STATE1: self.state1,
            States.STATE2: self.state2,
            States.STATE3: self.state3
        }

        return


    def run(self):
        self.state_machine[self.state]()
        return


    def start(self):
        self.main_ticker = br_timer.ticker(
            self.ticker_number, self.main_frequency, self.run)
        self.main_ticker.start() #i dont get why we have to do this line...
        return

    def stop(self):
        self.main_ticker.stop()
        return

    def state0(self):

        # Entry action
        if self.last_state != self.state:
            print('mode turnt into state 0')
            self.last_state = self.state

        # Action
        print('no leds are lighting up')

        # State guards (transitions)
        self.state = States.STATE1

        return


    def state1(self):
        # Entry action
        if self.last_state != self.state:
            print('mode turnt into state 1')
            self.last_state = self.state

        # Action
        print('led 1 is on')

        # State guards (transitions)
        self.state = States.STATE2


    def state2(self):
        # Entry action
        if self.last_state != self.state:
            print('mode turnt into state 2')
            self.last_state = self.state

        # Action
        print('led 2 is on')

        # State guards (transitions)
        self.state = States.STATE3

    def state3(self):
        # Entry action
        if self.last_state != self.state:
            print('mode turnt into state 3')
            self.last_state = self.state

        # Action
        print('led 3 is on')

        # State guards (transitions)
        self.state = States.STATE0



