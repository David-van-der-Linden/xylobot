from multiorderhighpass import Multiorderhighpass
from rmsfilter import Rmsfilter
from br_timer import *
from br_serial import *
from machine import Pin, ADC


class Calibration():
    """
    Class for calibration of the EMG-Signal
    --> run() to start the calibration process
    --> stop_calibration() to end the calibration process
    --> get_calibration_result_left()  get back the max Value that occured during the calibration process
    --> get_calibration_result_right()
    The EMG-Signal is filtered with an highpassfilter and a rmsfilter

    """

    def __init__(self, sampling_frequency, cutoff_frequency, filter_order, calibration_pin_left, calibration_pin_right,
                 static_gain, rmsfilter_window_size):
        self.sampling_frequency = sampling_frequency
        self.cutoff_frequency = cutoff_frequency
        self.filter_order = filter_order
        self.calibration_result_left = 0
        self.calibration_result_right = 0
        self.calibration_pin_left = calibration_pin_left
        self.calibration_pin_right = calibration_pin_right
        self.static_gain = static_gain
        self.rmsfilter_window_size = rmsfilter_window_size

        self.t1 = ticker(1, self.sampling_frequency, self.loop)
        self.mohpL = Multiorderhighpass(self.filter_order, self.sampling_frequency, self.cutoff_frequency,
                                        self.static_gain)
        self.rmsfL = Rmsfilter(self.rmsfilter_window_size)
        self.mohpR = Multiorderhighpass(self.filter_order, self.sampling_frequency, self.cutoff_frequency,
                                        self.static_gain)
        self.rmsfR = Rmsfilter(self.rmsfilter_window_size)

    def run(self):
        self.calibration_result_left = 0
        self.calibration_result_right = 0
        self.t1.start()
        return

    def loop(self):
        adcL = ADC(Pin(self.calibration_pin_left))
        new_value_left = self.rmsfL.process(abs(self.mohpL.process(adcL.read_u16())))
        if self.calibration_result_left < new_value_left:
            self.calibration_result_left = new_value_left

        adcR = ADC(Pin(self.calibration_pin_right))
        new_value_right = self.rmsfR.process(abs(self.mohpR.process(adcR.read_u16())))
        if self.calibration_result_right < new_value_right:
            self.calibration_result_right = new_value_right

        return

    def stop_calibration(self):
        self.t1.stop()
        return

    def get_calibration_result_left(self):
        return round(self.calibration_result_left)

    def get_calibration_result_right(self):
        return round(self.calibration_result_right)
