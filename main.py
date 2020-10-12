import sys
sys.path.append('../micropython_dummy_modules/')
from modecontrol import Modecontroler


if __name__ == '__main__':
    new_controler = Modecontroler(1, 1)

    new_controler.start()
