from emgInput import EmgInput
import utime

class RefrenceXY(object):
    def __init__(self, xpos, ypos, loopfrq, calibrationLeft, calibrationRight, cutoff_frequency, rmsfilter_window_size, filter_order):
        # initial position
        self.xpos = xpos
        self.ypos = ypos
        # start out moving up
        self.emgR = False
        self.emgL = True
        # making bounds known
        self.xbound = 7
        self.ybound = 35
        # movement Stepsize
        self.generalStepsize = 12 / loopfrq  # cm per second / loopfrq
        self.upStepsize = self.generalStepsize*2
        self.downStepsize = self.generalStepsize
        self.horizontalStepsize = self.generalStepsize*5
        # emg
        self.emgInput = EmgInput(loopfrq, filter_order, calibrationLeft, calibrationRight, cutoff_frequency, rmsfilter_window_size)
    
    def changeInput(self,left,right):
        
        self.emgR= right
        self.emgL = left
    def updateInput(self):
        #self.emgR = self.emgInput.getEmgRight()
        #self.emgL = self.emgInput.getEmgLeft()
        #self.emgR = False
        #self.emgL = True
        # print("left:", self.emgL, ", right:", self.emgR)
        if self.emgL:
            if self.emgR:
                self.moveDown()
                # print("Go Down")
            else:
                self.moveUp()
                self.moveLeft()
                # print("Go Left (and up)")
        elif self.emgR:
            self.moveUp()
            self.moveRight()
            # print("Go Right (and up)")
        else:
            self.moveUp()
            # print("Go up")
        return

    def moveUp(self):
        if self.xpos > self.upStepsize:
            self.xpos = self.xpos - self.upStepsize
        # print('up')
        return

    def moveDown(self):
        if self.xpos < self.xbound - self.downStepsize:
            self.xpos = self.xpos + self.downStepsize
        # print('down')
        return

    def moveLeft(self):
        if self.ypos < self.ybound - self.horizontalStepsize:
            self.ypos = self.ypos + self.horizontalStepsize
        # print('left')
        return

    def moveRight(self):
        if self.ypos > self.horizontalStepsize:
            self.ypos = self.ypos - self.horizontalStepsize
        # print('right')
        return

    def setRef(self,x,y):
        self.xpos = x
        self.ypos = y
        return

    def getRefrenceXYPosition(self):
        self.updateInput()
        return round(self.xpos, 2), round(self.ypos, 2)
