
import br_serial
from potmeter import Potmeter
from motor import Motor
from biquad import Biquad
from unwrapper import Unwrapper
from pid_controller import PID_pf
from pid_controller_2 import PID_2
import math


class StateFunctions(object):


    def __init__(self, motor_freq):
        #self.state_object = state_object
        self.potmeter1 = Potmeter(meter=1)
        self.motor1 = Motor(motor_freq, motor=1, encoder_period=8400)
        #self.potmeter2 = Potmeter(meter=2)
        self.motor2 = Motor(motor_freq, motor=2, encoder_period=8400)
        self.serial_pc = br_serial.serial_pc(4)
        
        # For encoders
        self.unwrapper1 = Unwrapper(2**16)
        self.unwrapper2 = Unwrapper(2**16)
        self.filter_enc1 = Biquad(
            (1, -1.142980502539901, 0.412801598096189), (1, 2, 1))
        self.filter_enc2 = Biquad(
            (1, -1.142980502539901, 0.412801598096189), (1, 2, 1))
    	self.p1 = 300
        self.i1 = 5
        self.d1 = 2
        self.p2 = 150 #asymmetric because more friction on right motor
        self.i2 = 5
        self.d2 = 1
        self.pid = PID_pf(1 / motor_freq, self.p1, self.i1, self.d1)
        self.pid2 = PID_2(1 / motor_freq, self.p2, self.i2, self.d2)
        self.initial_degree1 = 90
        self.initial_degree2 = 90
        self.duty2 =0
        self.duty_cycle=0
        return


    def safe(self):
        # Entry action
        #if self.state_object.is_new_state():
        #print('Entered SAFE')

        # Action
        self.motor1.pulse_width_percent(0)
        self.motor2.pulse_width_percent(0)
        # State guards
        # None: performed by the button press
        return

    def motorMoving(self):
        print("DutyCycle:",self.duty_cycle,self.duty2)
        if self.duty_cycle<20 and self.duty2<15:
            return False
        else :
            return True

    def read(self):
        # Entry action
        if self.state_object.is_new_state():
            print('Entered READ')

        # Read potmeter value
        #pot_value = self.potmeter1.read()

        # Read encoder value and unwrap it
        
        measured = self.unwrapper1.unwrap(self.motor1.read_encoder_count()) +8400*(self.initial_degree1 /360)#unwrapper function
        m2=self.unwrapper2.unwrap(self.motor2.read_encoder_count())+8400*(self.initial_degree2 /360)
        
        print("Encoder1:",measured)
        #print("Encoder1 without unwrap:",measuredn)
        print("Encoder2:",m2)
        #print("Encoder2 without unwrap:",m2n)

        # Send both over serial
        # self.serial_pc.set(0, pot_value)
        # self.serial_pc.set(1, enc_value)
        # self.serial_pc.send()
        #print("potmeter1:", self.serial_pc.set(0, pot_value))


        # State guards
        # None: performed by the button press
        return

    
    def on(self,x_new,y_new):
        # Entry action
        #if self.state_object.is_new_state():
        #print('Entered ON')
        # # Read potmeter and scale value to +- 8400 counts
        #reference = self.potmeter1.read() * 2 * 8400 / (2**16 - 1) - 8400 #
        # angle = count/8400 
        reference = ((self.pid.angles_motor_1(x_new,y_new))/360)*8400 #change 100,300 to x_new and y_new
        ref2 = ((self.pid2.angles_motor_2(x_new,y_new))/360)*8400
        # # Read encoder and unwrap its value
        measured = self.unwrapper1.unwrap(self.motor1.read_encoder_count()) +8400*(self.initial_degree1 /360)#unwrapper function
        m2=self.unwrapper2.unwrap(self.motor2.read_encoder_count())+8400*(self.initial_degree2 /360)
        # # Feed reference and measured to PID, pass biquad filter callable
        control_output = self.pid.step(
            reference, measured, filtfun=self.filter_enc1.step)
        control2=self.pid2.step(
            ref2, m2, filtfun=self.filter_enc2.step)
        # Set motor direction depending on sign of control_output
        # NOTE that spinning the motor must not move the encoder count further
        # away from the reference!
        if ((control_output > 0 and not self.motor1.direction_pin.value()) or
                (control_output < 0 and self.motor1.direction_pin.value())):
            self.motor1.reverse()

        if ((control2 > 0 and not self.motor2.direction_pin.value()) or
                (control2 < 0 and self.motor2.direction_pin.value())):
            self.motor2.reverse()
        # Convert control output to a duty cycle and apply to motor
        # Here scaled such that 8400 counts offset corresponds to 100% pwm
        # when using only a p_gain. Capped at 100% duty cycle.
        self.duty_cycle = abs(control_output) * 100 / (self.pid.p_gain * 8400) *13
        self.duty2=abs(control2) * 100 / (self.pid2.p_gain * 8400)*13

        #enc_value = self.unwrapper1.unwrap(self.motor1.read_encoder_count())
        #enc2 = self.unwrapper2.unwrap(self.motor2.read_encoder_count())
        #print("encoder1",enc_value)
        #print("encoder2",enc2)

        if self.duty_cycle > 100:
            self.duty_cycle = 100
        self.motor1.pulse_width_percent(self.duty_cycle)
        if self.duty2 > 100:
            self.duty2 = 100
        self.motor2.pulse_width_percent(self.duty2)
        self.serial_pc.set(0, reference)
        self.serial_pc.set(1, measured)
        self.serial_pc.set(2, ref2)
        self.serial_pc.set(3, m2)
        #print("M1",measured)
       # print("Ref1",reference)
        #print("M2",m2)
        #print("Ref2",ref2)
        self.serial_pc.send()
        # State guards
        # None: performed by the button press
        return



