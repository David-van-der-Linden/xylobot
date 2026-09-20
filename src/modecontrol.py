from statesIN import StatesIN
from br_serial import *
import pyb


class Modecontroler(object):

    def __init__(self, refrenceobject):
        self.last_state = StatesIN.STATE3  # for smoother sailing but: None is also a good alternative
        self.state = StatesIN.STATE0  # initial state
        self.globalstate = 0
        self.state_machine = {
            StatesIN.STATE0: self.state0,
            StatesIN.STATE1: self.state1,
            StatesIN.STATE2: self.state2,
            StatesIN.STATE3: self.state3
        }
        # switch tings
        self.sw = pyb.Switch()
        self.sw.callback(self.run)
        self.led1 = pyb.LED(1)
        self.led2 = pyb.LED(2)
        self.led3 = pyb.LED(3)
        self.refrenceobject = refrenceobject
        return

    def run(self):  # does one iteration
        self.state_machine[self.state]()
        return

    def state0(self):
        # Entry action

        # Action
        # led thing
        print('no leds are lighting up')
        self.led1.off()
        self.led2.off()
        self.led3.off()
        # non led thing
        self.globalstate = 0

        # State guards (transitions)
        if self.last_state == StatesIN.STATE1:
            self.last_state = StatesIN.STATE0
            self.state = StatesIN.STATE2
        elif self.last_state == StatesIN.STATE2:
            self.last_state = StatesIN.STATE0
            self.state = StatesIN.STATE3
        elif self.last_state == StatesIN.STATE3:
            self.last_state = StatesIN.STATE0
            self.state = StatesIN.STATE1
        else:
            print('no last state found sending to state 1')
            self.last_state = StatesIN.STATE0
            self.state = StatesIN.STATE1

        return

    def state1(self):
        # Entry action
        # led thing
        print('led 1 is on')
        self.led1.on()
        self.led2.off()
        self.led3.off()
        # non led thing
        self.globalstate = 1
        # print('were calling the fuction state 1', 'and globalstate is:', self.globalstate)
        self.refrenceobject.xpos = 7      # diffrent values might be better here
        self.refrenceobject.ypos = 17.5   # "
        # Actions

        # State guards (transitions)
        self.last_state = StatesIN.STATE1
        self.state = StatesIN.STATE0
        return

    def state2(self):
        # Entry action
        if self.last_state != self.state:
            # making sure song plays from start again
            # todo make code more sexy by adding reset fuction inside of the refrencexy.py class
            self.refrenceobject.songIsOver = False
            self.refrenceobject.songTime = 0
            self.refrenceobject.timeToStartMovingToHitTheNextNote = 0
            self.refrenceobject.noteNumber = 0
            self.timeProbbeblyHitNoteByNow = None
            # historic code
            self.last_state = self.state

        # Action
        # led thing
        print('led 2 is on')
        self.led1.off()
        self.led2.on()
        self.led3.off()
        # non led things
        self.globalstate = 2

        # State guards (transitions)
        self.last_state = StatesIN.STATE2
        self.state = StatesIN.STATE0
        return

    def state3(self):  # this state is currently not in use
        # Entry action
        if self.last_state != self.state:
            # print('mode turned into state 3') #not necessary since we allays switch
            self.last_state = self.state

        # Action
        # led things
        print('led 3 is on')
        self.led1.off()
        self.led2.off()
        self.led3.on()
        # non led things
        self.globalstate = 3

        # State guards (transitions)
        self.last_state = StatesIN.STATE3
        self.state = StatesIN.STATE0
        return

    def pls_give_state(self):
        # print('state according to modecontrol.py:', self.globalstate)
        return self.globalstate
