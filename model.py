from audio import myspectrogram

class model:
    def __init__(self):
        self.__posList=[]
        self.__size=1
        self.__sizeFreq=1
        self.__rank=1
        self.__erase=False

    def changeAudio(self,fileName,window):
        self.__Audio=myspectrogram(fileName,window)
        self.__Audio.drawFreq()
    
    def play(self):
        self.__Audio.play()

    def save(self,direction):
        self.__Audio.save(direction)
    
    def addPos(self,x,y):
        self.__posList.append([x,y])
    
    def clear(self):
        self.__Audio.filtering(self.__rank,self.__sizeFreq,self.__erase,self.__posList[0][0],self.__posList[0][1],self.__posList[1][0],self.__posList[1][1])
        self.__Audio.drawFreq()
        self.__posList=[]
        
    
    
    def setSizeFreq(self,value):
        self.__sizeFreq=float(value)
    
    def setPictureSize(self,size):
        self.__picSize=size

    def getPictureSize(self):
        return self.__picSize

    def setErase(self,value):
        self.__erase=value
    
    def setRank(self,value):
        self.__rank=float(value)