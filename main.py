# dummy modules
import sys

sys.path.append('../micropython_dummy_modules')  # todo test if this can be there while running on the mycrocontroler
# class import
from modecontrol import Modecontroler
# imports for testing sake #nm we use this shit now :(
import br_timer
from refrencexy import RefrenceXY
# comment for git testing sake

def callbackfunctionstate1():  # ordering problem solution 1
    itsrobertsfault = new_controler.pls_give_state()
    if itsrobertsfault == 1:  # state == 1
        print(refrenxycobject.getRefrenceXYPosition())  # gets disired xy positions
    # todo transform disierd xy to PRC
    # todo get the status of the motor angles
    # todo run pid regulation
    return


mainFreq = 100  # Hz
tickerState1 = br_timer.ticker(5, mainFreq, callbackfunctionstate1, GC=True)  # ordering problem solution 2
refrenxycobject = RefrenceXY(5, 0)  # ordering problem solution 3
new_controler = Modecontroler()

if __name__ == "__main__":
    print('Buckle up! It\'s going to be a bumpy ride!')
    tickerState1.start()  # ordering problem solution 4
