# dummy modules
import sys

sys.path.append('../micropython_dummy_modules')
# class import
from modecontrol import Modecontroler
# imports for testing sake #nm we use this shit now :(
import br_timer
from refrencexy import RefrenceXY
# emg specific imports
from calibration import Calibration
import utime

# angle transformation imports 
from angle_transformation import angles_motor_1, angles_motor_2


from timer_definitions import Timers
from state_functions import StateFunctions

main_frequency = 100 #hz
# Create MotorControl Object
motorControl = StateFunctions(main_frequency)

# EMG calibration
mainFreq = main_frequency  # Hz
cutoff_frequency, rmsfilter_window_size, filter_order = 20, 40, 3
calibration_pin_left, calibration_pin_right, static_gain = 'A0', 'A1', 1
newemgcalibrationobject = Calibration(mainFreq, cutoff_frequency, filter_order, calibration_pin_left,
                                      calibration_pin_right, static_gain, rmsfilter_window_size)
newemgcalibrationobject.run()
calibration_time = 10# Duration of calibration in seconds
for i in range(0,9):
    utime.sleep(calibration_time/10) 
    print("Calibration..")
 
newemgcalibrationobject.stop_calibration()
calibrationLeft = newemgcalibrationobject.get_calibration_result_left()
calibrationRight = newemgcalibrationobject.get_calibration_result_right()
print("calibration left:", calibrationLeft)
print("calibration right:", calibrationRight)


#start robot
motorControl = StateFunctions(main_frequency)




# main loop
def callbackfunctionstate1():  # ordering problem solution 1
    itsrobertsfault = new_controler.pls_give_state()
    #itsrobertsfault = 1
    if itsrobertsfault == 1:  # state == 1
        # print(refrenxycobject.getRefrenceXYPosition())
        x_old, y_old = refrenxycobject.getRefrenceXYPosition()  # gets disired xy positions
        x_new = 8.5 * (y_old - 17.5)  # 8 so that we make the math harder
        y_new = 10 * (x_old + 29.5)
        motorControl.on(x_new, y_new)
       
        #Enter On() state
        # print(x_new,y_new)
        
        #print("motor angels:", angles_motor_1(x_new, y_new), angles_motor_2(x_new, y_new))
    if itsrobertsfault == 0:
        motorControl.safe()

    elif itsrobertsfault == 2:
        x_new, y_new = refrenxycobject.getRefrenceXYPositionSong()
        # print(x_new, y_new)
        motorControl.on(x_new, y_new)
        # print("motor angels:", angles_motor_1(x_new, y_new), angles_motor_2(x_new, y_new))
    return


# ticker
tickerState1 = br_timer.ticker(5, mainFreq, callbackfunctionstate1, GC=True)  # ordering problem solution 2

# refrenceobject
refrenxycobject = RefrenceXY(7, 17.5, mainFreq, calibrationLeft, calibrationRight, cutoff_frequency, rmsfilter_window_size,
                             filter_order)  # ordering problem solution 3
#7,17.5
# state machine
new_controler = Modecontroler(refrenxycobject)

if __name__ == "__main__":
    print('Buckle up! It\'s going to be a bumpy ride!')
    tickerState1.start()  # ordering problem solution 4
    #utime.sleep(15)
    #refrenxycobject.changeInput(False,True)

