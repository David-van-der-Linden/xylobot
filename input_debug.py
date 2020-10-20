# Use one of the filters on a user button input and send result to uScope
from br_timer import *
from br_serial import *
from machine import Pin, ADC

from multiorderhighpass import Multiorderhighpass 
from rmsfilter import Rmsfilter

loop_frequency = 100
pc = serial_pc(3)
mohp= Multiorderhighpass(3,loop_frequency,20,1)    #Filter order, sampling frequency, cutoff frequency, Static Gain
rmsf= Rmsfilter(50)    #Number of processed values
calibration_result= 50000 # This Number has to be messured in the Calibration process 


def loop():
    adc = ADC(Pin('A0'))
 # Read value of 16bit ADC between 0-65535 corresponding to 0V-3.3V

    pc.set(0, adc.read_u16())
    pc.set(1,mohp.process(adc.read_u16()))
    pc.set(2,rmsf.process(abs(mohp.process(adc.read_u16()))))
    print(mohp.process(adc.read_u16()))
    pc.send()
t1 = ticker(1, loop_frequency, loop)
t1.start()