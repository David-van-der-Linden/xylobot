from states import States
from br_serial import *
import pyb


class Modecontroler(object):

    def __init__(self):
        self.last_state = States.STATE3  # for smoother sailing but: None is also a good alternative
        self.state = States.STATE0  # initial state
        self.globalstate = 0
        self.state_machine = {
            States.STATE0: self.state0,
            States.STATE1: self.state1,
            States.STATE2: self.state2,
            States.STATE3: self.state3
        }
        # switch tings
        self.sw = pyb.Switch()
        self.sw.callback(self.run)
        return

    def run(self):  # does one iteration
        self.state_machine[self.state]()
        return

    def state0(self):
        # Entry action

        # Action
        print('no leds are lighting up')  # todo actually off on the leds
        self.globalstate = 0

        # State guards (transitions) # todo update to include state 4
        if self.last_state == States.STATE1:
            self.last_state = States.STATE0
            self.state = States.STATE2
        elif self.last_state == States.STATE2:
            self.last_state = States.STATE0
            self.state = States.STATE3
        elif self.last_state == States.STATE3:
            self.last_state = States.STATE0
            self.state = States.STATE1
        else:
            print('no last state found sending to state 1')
            self.last_state = States.STATE0
            self.state = States.STATE1

        return

    def state1(self):
        # Entry action
        print('led 1 is on')  # todo actually turn on the led
        self.globalstate = 1
        print('were calling the fuction state 1', 'and globalstate is:', self.globalstate)

        # Actions

        # State guards (transitions)
        self.last_state = States.STATE1
        self.state = States.STATE0
        return

    def state2(self):
        # Entry action
        if self.last_state != self.state:  # todo check if this needs to be here
            # print('mode turned into state 2') #not necessary since we allays switch
            self.last_state = self.state
            # todo run initialisation sequence
        # todo same as above state but there is a change to the reference

        # Action
        print('led 2 is on')  # todo actually turn on the led
        self.globalstate = 2

        # State guards (transitions)
        self.last_state = States.STATE2
        self.state = States.STATE0
        return

    def state3(self):
        # Entry action
        if self.last_state != self.state:
            # print('mode turned into state 3') #not necessary since we allays switch
            self.last_state = self.state
            # todo run initialisation sequence

        # Action
        print('led 3 is on')  # todo actually turn on the led
        self.globalstate = 3
        # todo run set of pre-programed moments

        # State guards (transitions)
        # todo change to a press of the button
        self.last_state = States.STATE3
        self.state = States.STATE0
        return

    def pls_give_state(self):
        # print('state according to modecontrol.py:', self.globalstate)
        return self.globalstate
