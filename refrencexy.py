from emgInput import EmgInput


class RefrenceXY(object):
    def __init__(self, xpos, ypos, loopfrq, calibrationLeft, calibrationRight, cutoff_frequency, rmsfilter_window_size, filter_order):
        # initial position
        self.xpos = xpos
        self.ypos = ypos
        # start out moving up
        self.emgR = False
        self.emgL = False
        # making bounds known
        self.xbound = 5
        self.ybound = 35
        # movement Stepsize
        self.generalStepsize = 0.01  # todo make this dependent on freqency
        self.upStepsize = self.generalStepsize
        self.downStepsize = self.generalStepsize
        self.horizontalStepsize = self.generalStepsize
        # emg
        self.emgInput = EmgInput(loopfrq, filter_order, calibrationLeft, calibrationRight, cutoff_frequency, rmsfilter_window_size)

    def updateInput(self):
        self.emgR = self.emgInput.getEmgRight()
        self.emgL = self.emgInput.getEmgLeft()
        if self.emgL:
            if self.emgR:
                self.moveDown()
            else:
                self.moveUp()
                self.moveLeft()
        elif self.emgR:
            self.moveUp()
            self.moveRight()
        else:
            self.moveUp()
        return

    def moveUp(self):
        if self.xpos > self.upStepsize:
            self.xpos = self.xpos - self.upStepsize
        return

    def moveDown(self):
        if self.xpos < self.xbound - self.downStepsize:
            self.xpos = self.xpos + self.downStepsize
        return

    def moveLeft(self):
        if self.ypos < self.ybound - self.horizontalStepsize:
            self.ypos = self.ypos + self.horizontalStepsize
        return

    def moveRight(self):
        if self.ypos > self.horizontalStepsize:
            self.ypos = self.ypos - self.horizontalStepsize
        return

    def getRefrenceXYPosition(self):
        self.updateInput()
        return(self.xpos, self.ypos)
