class Sonar:
    def __init__(self, position=(0,0), waveList=[]):
        #Sonar Position
        self.postion = position
        self.Xi, self.Yi = position

        #Objects detected
        self.waveList = waveList