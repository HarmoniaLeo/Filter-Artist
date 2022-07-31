from pyAudioKits.audio import read_Audio
from pyAudioKits.analyse import FFT
from pyAudioKits.filters import lowPassButterN, highPassButterN, bandPassButterN, bandStopButterN
import matplotlib.pyplot as plt
import numpy as np

class myspectrogram:
    def __init__(self,direction,window):
        self.__wav = read_Audio(direction)
        self.__M=0.03
        self.__R=0.015

        if window=="Hamming":
            self.__Window = "hamming"
        elif window=="Rectangle":
            self.__Window = None

    def __stft(self):
        self.__freq = FFT(self.__wav.framing(self.__M, 1 - self.__R/self.__M, self.__Window))
    
    def save(self,direction):
        self.__wav.save(direction)
    
    def play(self):
        self.__wav.sound()

    def drawFreq(self):
        self.__stft()
        plt.figure(figsize=(8,2))
        plt.axis('off')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        self.__freq.plot(ax=plt.gca(),cbar=False,freq_scale="mel",plot_type="dB")
        plt.savefig("tmp.png")
        # img=cv2.imread("tmp.png")
        # img=cv2.resize(img,)
        # cv2.imwrite("tmp.png",img)

    def filtering(self,n,sizeFreq,erase,xposeStart,yposeStart,xposeEnd,yposeEnd):
        def freq_transform(freq):
            sr = self.__wav.sr
            length = int(self.__M  * sr / 2)
            max_freq_point = int(sr / 2)
            max_freq = sr / 2
            freq_points = 700 * (np.power(10, np.linspace(0, 2595 * np.log10(1 + max_freq/700), length)/2595) - 1)
            freq_point = freq_points[int(length * freq)]
            freqs = np.linspace(0,max_freq,max_freq_point)
            return freqs[int(freq_point)]

        xsize=self.__R * self.__freq.shape[0]
        xposeStart=xsize*xposeStart
        xposeEnd=xsize*xposeEnd

        yposeNow=float(yposeStart)
        width=float(sizeFreq)/200

        low=yposeNow-width
        high=yposeNow+width

        if erase:
            if low>0 and high<1:
                filt = lambda x: bandStopButterN(x, n, freq_transform(low), freq_transform(high))
            if low<=0:
                filt = lambda x: highPassButterN(x, n, freq_transform(high))
            if high>=1:
                filt = lambda x: lowPassButterN(x, n, freq_transform(low))
        else:
            if low>0 and high<1:
                filt = lambda x: bandPassButterN(x, n, freq_transform(low), freq_transform(high))
            if low<=0:
                filt = lambda x: lowPassButterN(x, n, freq_transform(high))
            if high>=1:
                filt = lambda x: highPassButterN(x, n, freq_transform(low))
        if xposeStart<xposeEnd:
            self.__wav[xposeStart:xposeEnd]=filt(self.__wav[xposeStart:xposeEnd])
        if xposeEnd<xposeStart:
            self.__wav[xposeEnd:xposeStart]=filt(self.__wav[xposeEnd:xposeStart])
        