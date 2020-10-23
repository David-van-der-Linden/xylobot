# dummy modules
import sys

sys.path.append('../micropython_dummy_modules')  # todo test if this can be there while running on the mycrocontroler
# class import
from modecontrol import Modecontroler
# imports for testing sake #nm we use this shit now :(
import br_timer
from refrencexy import RefrenceXY
# emg specific imports
from calibration import Calibration
import utime

# EMG calibration
mainFreq = 100  # Hz
cutoff_frequency, rmsfilter_window_size, filter_order = 20, 50, 4
calibration_pin_left, calibration_pin_right, static_gain = 'A0', 'A1', 1
newemgcalibrationobject = Calibration(mainFreq, cutoff_frequency, filter_order, calibration_pin_left,calibration_pin_right,static_gain,rmsfilter_window_size)
newemgcalibrationobject.run()
utime.sleep(20)
newemgcalibrationobject.stop_calibration()
calibrationLeft = newemgcalibrationobject.get_calibration_result_left()
calibrationRight = newemgcalibrationobject.get_calibration_result_right()
print(calibrationLeft)
print(calibrationRight)

# main loop
def callbackfunctionstate1():  # ordering problem solution 1
    itsrobertsfault = new_controler.pls_give_state()
    if itsrobertsfault == 1:  # state == 1
        print(refrenxycobject.getRefrenceXYPosition())  # gets disired xy positions
    # todo transform disierd xy to PRC
    # todo get the status of the motor angles
    # todo run pid regulation
    return

# ticker
tickerState1 = br_timer.ticker(5, mainFreq, callbackfunctionstate1, GC=True)  # ordering problem solution 2

# refrenceobject
refrenxycobject = RefrenceXY(5, 0, mainFreq, calibrationLeft, calibrationRight, cutoff_frequency, rmsfilter_window_size, filter_order)  # ordering problem solution 3

# state machine
new_controler = Modecontroler()

if __name__ == "__main__":
    print('Buckle up! It\'s going to be a bumpy ride!')
    tickerState1.start()  # ordering problem solution 4
