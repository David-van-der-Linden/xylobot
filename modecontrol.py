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
        self.main_ticker.start()  # i dont get why we have to do this line...
        return

    def stop(self):
        self.main_ticker.stop()
        return

    def state0(self):

        # Entry action
        if self.last_state != self.state:
            # print('mode turned into state 0') #not necessary since we allays switch
            self.last_state = self.state
            # todo turn off things from previous state if neccecary

        # Action
        print('no leds are lighting up')  # todo actually off on the leds

        # State guards (transitions)
        self.state = States.STATE1

        return

    def state1(self):
        # Entry action
        if self.last_state != self.state:
            # print('mode turned into state 1') #not necessary since we allays switch
            self.last_state = self.state
            # todo run initialisation sequence

        # Action
        print('led 1 is on')  # todo actually turn on the led
        # todo change reference based on emg signal input
        # todo use desired X-Y t
        # todo use kinematics to find the dizered motor control outputs

        # todo finish this todo list

        # State guards (transitions)
        # todo change to a press of the button
        self.state = States.STATE2

    def state2(self):
        # Entry action
        if self.last_state != self.state:
            # print('mode turned into state 2') #not necessary since we allays switch
            self.last_state = self.state
        # todo run initialisation sequence
        # todo same as above state but there is a change to the reference

        # Action
        print('led 2 is on')  # todo actually turn on the led

        # State guards (transitions)
        # todo change to a press of the button
        self.state = States.STATE3

    def state3(self):
        # Entry action
        if self.last_state != self.state:
            # print('mode turned into state 3') #not necessary since we allays switch
            self.last_state = self.state
            # todo run initialisation sequence

        # Action
        print('led 3 is on')  # todo actually turn on the led
        # todo run set of pre-programed moments

        # State guards (transitions)
        # todo change to a press of the button
        self.state = States.STATE0
