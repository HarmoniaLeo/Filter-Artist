import librosa
import librosa.display
from pyaudio import PyAudio, paInt16
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import wave
import numpy as np
import cv2
from playsound import playsound
from scipy.signal import butter,filtfilt,lfilter,firwin,sosfiltfilt

class myspectrogram:
    def __init__(self,direction,window):
        self.__wav,self.__sr=librosa.load(direction)
        self.__M=64
        self.__R=64

        if window=="Hamming":
            self.__Window=np.hamming(M=self.__M)
        elif window=="Rectangle":
            self.__Window=np.ones(self.__M)

    def __stft(self):
        fs=[]
        for i in range(0,self.__wav.shape[0]-self.__M+1,self.__R): #步长1024
            fs.append(fft(self.__wav[i:i+self.__M]*self.__Window))
        self.__freq=np.array(fs)
    
    def save(self,direction):
        librosa.output.write_wav(direction,np.ascontiguousarray(self.__wav),self.__sr)
    
    def play(self):
        librosa.output.write_wav("tmp.wav",np.ascontiguousarray(self.__wav),self.__sr)
        playsound("tmp.wav")

    def drawFreq(self):
        self.__stft()
        freq=(self.__freq).T
        freq=freq[:int(freq.shape[0]/2)]
        plt.axis('off')
        plt.gca().xaxis.set_major_locator(plt.NullLocator())
        plt.gca().yaxis.set_major_locator(plt.NullLocator())
        plt.subplots_adjust(top = 1, bottom = 0, right = 1, left = 0, hspace = 0, wspace = 0)
        plt.margins(0,0)
        librosa.display.specshow(librosa.amplitude_to_db(np.abs(freq)))
        plt.savefig("tmp.png")
        img=cv2.imread("tmp.png")
        img=cv2.resize(img,(self.__freq.shape[0],int(self.__freq.shape[1]/2)))
        cv2.imwrite("tmp.png",img)


    def filtering(self,n,sizeFreq,erase,xposeStart,yposeStart,xposeEnd,yposeEnd):

        xsize=self.__freq.shape[0]
        xposeStart=int(xsize*xposeStart)*self.__R
        xposeEnd=int(xsize*xposeEnd)*self.__R

        yposeNow=float(yposeStart)
        width=float(sizeFreq)/200

        low=1-yposeNow-width
        high=1-yposeNow+width
        

        if erase:
            if low>0 and high<1:
                sos=butter(n,[low,high],btype='bandstop',output='sos')
            if low<=0:
                sos=butter(n,high,btype='highpass',output='sos')
            if high>=1:
                sos=butter(n,low,btype='lowpass',output='sos')
        else:
            if low>0 and high<1:
                sos=butter(n,[low,high],btype='bandpass',output='sos')
            if low<=0:
                sos=butter(n,high,btype='lowpass',output='sos')
            if high>=1:
                sos=butter(n,low,btype='highpass',output='sos')
        if xposeStart<xposeEnd:
            self.__wav[xposeStart:xposeEnd]=sosfiltfilt(sos,self.__wav[xposeStart:xposeEnd])
        if xposeEnd<xposeStart:
            self.__wav[xposeEnd:xposeStart]=sosfiltfilt(sos,self.__wav[xposeEnd:xposeStart])
        