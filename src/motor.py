
from pin_definitions import Pins
from machine import Pin
from pyb import Timer
from timer_definitions import Timers


class Motor(object):

    def __init__(self, freq, motor, encoder_period):

        if motor == 1:
            # Configure driver pins
            pin = Pin(Pins.MOTOR1_PWM, Pin.OUT)
            timer_pwm = Timer(Timers.MOTOR1_PWM, freq=freq)
            self.pwm_pin = timer_pwm.channel(
                Timers.MOTOR1_PWM_CHANNEL, Timer.PWM, pin=pin)
            self.direction_pin = Pin(Pins.MOTOR1_DIRECTION, Pin.OUT)

            # Configure encoder pins
            #pin_a = Pin(Pins.MOTOR1_ENC_A, Pin.AF_PP)
            #pin_b = Pin(Pins.MOTOR1_ENC_B, Pin.AF_PP)
            self.timer_enc = Timer(
                Timers.MOTOR1_ENC, prescaler=0, period=0xFFFF)
            self.timer_enc.channel(
                Timers.MOTOR1_ENC_A_CHANNEL, Timer.ENC_AB, pin=Pin('D0'))
            self.timer_enc.channel(
                Timers.MOTOR1_ENC_B_CHANNEL, Timer.ENC_AB, pin=Pin('D1'))

            # Configure the timer to count 2^16 numbers between [0, 65535]
                #encoder_2 = Timer(4, prescaler = 0, period = 0xFFFF)

# Configure the channels as encoders and attach the pins
                #encoder_2.channel(2, Timer.ENC_AB, pin = Pin('D0'))
                #encoder_2.channel(1, Timer.ENC_AB, pin = Pin('D1'))

        else:
            # Configure driver pins
            pin = Pin(Pins.MOTOR2_PWM, Pin.OUT)
            timer_pwm = Timer(Timers.MOTOR2_PWM, freq=freq)
            self.pwm_pin = timer_pwm.channel(
                Timers.MOTOR2_PWM_CHANNEL, Timer.PWM, pin=pin)
            self.direction_pin = Pin(Pins.MOTOR2_DIRECTION, Pin.OUT)

            # Configure encoder pins
            #pin_a = Pin(Pins.MOTOR2_ENC_A, Pin.AF_PP)
            #pin_b = Pin(Pins.MOTOR2_ENC_B, Pin.AF_PP)
            self.timer_enc = Timer(
                Timers.MOTOR2_ENC, prescaler=0, period=0xFFFF)
            self.timer_enc.channel(
                Timers.MOTOR2_ENC_A_CHANNEL, Timer.ENC_AB, pin=Pin('D12'))
            self.timer_enc.channel(
                Timers.MOTOR2_ENC_B_CHANNEL, Timer.ENC_AB, pin=Pin('D11'))

                #encoder_1 = Timer(3, prescaler = 0, period = 0xFFFF)

                # Configure the channels as encoders and attach the pins
                #encoder_1.channel(2, Timer.ENC_AB, pin = Pin('D12'))
                #encoder_1.channel(1, Timer.ENC_AB, pin = Pin('D11'))
        return


    def pulse_width_percent(self, percentage):
        # Just a wrapper function
        self.pwm_pin.pulse_width_percent(percentage)
        return


    def reverse(self):
        # Flip the value on the direction pin
        reverse_value = not self.direction_pin.value()
        self.direction_pin.value(reverse_value)
        return


    def read_encoder_count(self):
        return self.timer_enc.counter()
