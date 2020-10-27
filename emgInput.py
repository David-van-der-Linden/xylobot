from machine import Pin, ADC

from multiorderhighpass import Multiorderhighpass
from rmsfilter import Rmsfilter


class EmgInput():
    def __init__(self, loop_frequency, filter_order, calibration_result_left, calibration_result_right,
                 cutoff_frequency, rmsfilter_window_size):
        self.loop_frequency = loop_frequency
        self.filter_order = filter_order
        self.calibration_result_left = calibration_result_left  # This Number has to be messured in the Calibration process
        self.calibration_result_right = calibration_result_right  # This Number has to be messured in the Calibration process
        self.cutoff_frequency = cutoff_frequency
        self.rmsfilter_window_size = rmsfilter_window_size
        self.mohp1 = Multiorderhighpass(filter_order, loop_frequency, cutoff_frequency,
                                        1)  # Filter order, sampling frequency, cutoff frequency, Static Gain
        self.mohp2 = Multiorderhighpass(filter_order, loop_frequency, cutoff_frequency,
                                        1)  # Filter order, sampling frequency, cutoff frequency, Static Gain
        self.rmsf1 = Rmsfilter(rmsfilter_window_size)  # Number of processed values
        self.rmsf2 = Rmsfilter(rmsfilter_window_size)  # Number of processed values
        self.adc1 = ADC(Pin('A0'))
        self.adc2 = ADC(Pin('A1'))


    def getEmgLeft(self):  # This function needs to be called with the loop_frequency
        # Read value of 16bit ADC between 0-65535 corresponding to 0V-3.3V
        # Read value of 16bit ADC between 0-65535 corresponding to 0V-3.3V
        if (self.rmsf1.process(abs(self.mohp1.process(self.adc1.read_u16()))) / self.calibration_result_left) > 0.08:
            return True
        return False

    def getEmgRight(self):  # This function needs to be called with the loop_frequency
        # Read value of 16bit ADC between 0-65535 corresponding to 0V-3.3V
        if (self.rmsf2.process(abs(self.mohp2.process(self.adc2.read_u16()))) / self.calibration_result_right) > 0.08:
            return True
        return False
