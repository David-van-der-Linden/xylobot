"""
Create Robot state machine and run it with a ticker
"""

import sys
sys.path.append('../micropython_dummy_modules/')
from state_machine import Robot
from timer_definitions import Timers


timer_number = Timers.RUN
main_frequency = 20

robot = Robot(timer_number, main_frequency)
robot.start()