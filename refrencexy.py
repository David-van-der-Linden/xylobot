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

        # automatic song playing
        self.songIsOver = False
        self.motorIsMoving = None
        self.noteNumber = 0
        self.noteRefrenceState = None
        self.nextNote = None
        self.timeToStartMovingToHitTheNextNote = 0
        self.songTime = 0
        self.note_dic = {'C_1': -175, 'D_1': -148, 'E_1': -120, 'F_1': -90,
                         'G_1': -58, 'A_1': -29, 'B_1': 0, 'C_2': 29,
                         'D_2': 58, 'E_2': 87, 'F_2': 116, 'G_2': 145}  # in Clement's XYframe

        # List of songs in our arsonal
        self.song_twinkel = [('C_1', 1), ('C_1', 1), ('G_1', 1), ('G_1', 1), ('A_1', 1), ('A_1', 1), ('G_1', 2),
                             ('F_1', 1), ('F_1', 1), ('E_1', 1), ('E_1', 1), ('D_1', 1), ('D_1', 1), ('C_1', 2),
                             ('G_1', 1), ('G_1', 1), ('F_1', 1), ('F_1', 1), ('E_1', 1), ('E_1', 1), ('D_1', 2),
                             ('G_1', 1), ('G_1', 1), ('F_1', 1), ('F_1', 1), ('E_1', 1), ('E_1', 1), ('D_1', 2),
                             ('C_1', 1), ('C_1', 1), ('G_1', 1), ('G_1', 1), ('A_1', 1), ('A_1', 1), ('G_1', 2),
                             ('F_1', 1), ('F_1', 1), ('E_1', 1), ('E_1', 1), ('D_1', 1), ('D_1', 1), ('C_1', 2)]

        self.currentsong = self.song_twinkel
        self.durationQorterNote = loopfrq * 0.6  # 0.6 gives you around 100 BMP

    def changeInput(self,left,right):
        
        self.emgR = right
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

    def goAboveNote(self, note):  # todo use minimal jerk instead of step refrence so that the robot will break later
        self.xpos = self.note_dic.get(note) + 40  # so that it does not go out of bounds # todo make this less bodgey
        self.ypos = 300

    def updateInputSong(self, motorismovingpassingallongunnececerlylongnamesforthewin):
        if self.songIsOver:
            return
        self.motorIsMoving = False  # motorismovingpassingallongunnececerlylongnamesforthewin # todo undo this
        if self.songTime == 0:
            self.goAboveNote(self.currentsong[0][0])  # the first note
            self.noteRefrenceState = 'going to wait above note'
        elif self.noteRefrenceState == 'going to wait above note' and not self.motorIsMoving and self.songTime >= self.timeToStartMovingToHitTheNextNote:
            self.ypos = 320  # this will make it hit the note
            self.noteRefrenceState = 'going to hit note'
            self.timeToStartMovingToHitTheNextNote = self.songTime + self.durationQorterNote * \
                                                     self.currentsong[self.noteNumber + 1][1]
        elif self.noteRefrenceState == 'going to hit note' and not self.motorIsMoving:  # note has been hit
            self.noteNumber += 1
            if self.noteNumber >= len(self.currentsong):
                self.songIsOver = True
                return
            self.nextNote = self.currentsong[self.noteNumber][0]
            self.goAboveNote(self.nextNote)
            self.noteRefrenceState = 'going to wait above note'
        self.songTime += 1  # time the song has been playing in 100ths of a second if the loop frq is 100Hz
        return

    def getRefrenceXYPositionSong(self, motorismovingpassingallongunnececerlylongnamesforthewin):
        self.updateInputSong(motorismovingpassingallongunnececerlylongnamesforthewin)
        return round(self.xpos, 2), round(self.ypos, 2)