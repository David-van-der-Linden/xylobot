from refrencexy import RefrenceXY
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

    def run(self): # does one iteration
        self.state_machine[self.state]()
        return

    def start(self): # repeats iterations every second
        self.main_ticker = br_timer.ticker(
            self.ticker_number, self.main_frequency, self.run)
        self.main_ticker.start()  # i don't get why we have to do this line...
        return

    def stop(self):
        self.main_ticker.stop()
        return

    def state0(self):

        # Entry action


        # Action
        print('no leds are lighting up')  # todo actually off on the leds

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
        def callbackfunctionstate1(self): # todo check wheather this in the right spot
            refrenxycobject.getRefrenceXYPosition()  # gets disired xy positions
            # todo transform disierd xy to PRC
            # todo get the status of the motor angles
            # todo run pid regulation
            return

        print('led 1 is on')  # todo actually turn on the led
        refrenxycobject = RefrenceXY(5,0) #initial positions are given as paramaters
        tickerState1 = ticker(2, 100, callbackfunctionstate1(), GC=True)  # ticker number and ticker freqecy
        tickerState1.start()

        # Actions
        #for actions see callbackfunctoinstate1

        # State guards (transitions)
        # todo change to a press of the button
        self.last_state = States.STATE1
        self.state = States.STATE0
        tickerState1.ticker.stop()

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

