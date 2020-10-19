from refrencexy import RefrenceXY
from states import States
import br_timer
from br_serial import *
import pyb


class Modecontroler(object):

    def __init__(self):
        self.last_state = None
        self.state = States.STATE1
        self.state_machine = {
            States.STATE0: self.state0,
            States.STATE1: self.state1,
            States.STATE2: self.state2,
            States.STATE3: self.state3
        }
        # switch tings
        self.sw = pyb.Switch()
        self.sw.callback(self.run)
        # ticker things
        self.tickerState1 = br_timer.ticker(1, 100, self.callbackfunctionstate1, GC=True)  # todo let the ticker callback be globel to reduce error pocibilitys # ticker number and ticker freqecy, recomended:  1, 100
        # left overs
        self.refrenxycobject = RefrenceXY(5, 0) #initial positions are given as paramaters
        return

    def run(self):  # does one iteration
        self.state_machine[self.state]()
        return

    def state0(self):

        # Entry action

        # Action
        print('no leds are lighting up')  # todo actually off on the leds

        # State guards (transitions) # todo update to include state 4
        if self.last_state == States.STATE1:
            # turning of old part
            self.tickerState1.stop() #if this gives you problems try: self.tickerState1.ticker.stop()
            # moving on to next part
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

        self.tickerState1.start()

        print("ticker has been started")

        # Actions
        #for actions see callbackfunctoinstate1

        # State guards (transitions)
        # todo change to a press of the button
        self.last_state = States.STATE1
        self.state = States.STATE0
        return




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
        # todo run set of pre-programed moments

        # State guards (transitions)
        # todo change to a press of the button
        self.last_state = States.STATE3
        self.state = States.STATE0
        return

    def callbackfunctionstate1(self):  # todo check wheather this in the right spot
        print(self.refrenxycobject.getRefrenceXYPosition())  # gets disired xy positions
        # todo transform disierd xy to PRC
        # todo get the status of the motor angles
        # todo run pid regulation
        return

