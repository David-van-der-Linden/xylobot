
import sys
sys.path.append('../micropython_dummy_modules/')

from state_machine import Robot


ticker_number = 1
main_frequency = 20

robot = Robot(ticker_number, main_frequency)
robot.start()
