# Use one of the filters on a user button input and send result to uScope
from br_timer import *
from br_serial import *
from machine import Pin, ADC

from multiorderhighpass import Multiorderhighpass
from rmsfilter import Rmsfilter

loop_frequency = 100
pc = serial_pc(4)
mohp = Multiorderhighpass(5, loop_frequency, 20, 1)  # Filter order, sampling frequency, cutoff frequency, Static Gain
rmsf = Rmsfilter(100)  # Number of processed values
mohp2 = Multiorderhighpass(5, loop_frequency, 20, 1)  # Filter order, sampling frequency, cutoff frequency, Static Gain
rmsf2 = Rmsfilter(100)  # Number of processed values
calibration_result = 23000  # This Number has to be messured in the Calibration process
result_1 = 0
result_2 = 0


def loop():
    adc = ADC(Pin('A0'))
    adc2 = ADC(Pin('A1'))
    # Read value of 16bit ADC between 0-65535 corresponding to 0V-3.3V
    if (rmsf.process(abs(mohp.process(adc.read_u16()))) / calibration_result) > 0.08:
        result_1 = 1
    else:
        result_1 = 0

    if (rmsf2.process(abs(mohp2.process(adc2.read_u16()))) / calibration_result) > 0.08:
        result_2 = 1
    else:
        result_2 = 0
    # pc.set(0, adc.read_u16())
    # pc.set(0, mohp.process(adc.read_u16()))
    pc.set(0, (adc.read_u16()))
    pc.set(1, result_1)
    #pc.set(3, mohp2.process(adc2.read_u16()))
    pc.set(2, adc2.read_u16())
    pc.set(3, result_2)

    print(mohp.process(adc.read_u16()))
    pc.send()


t1 = ticker(1, loop_frequency, loop)
t1.start()
