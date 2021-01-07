import librosa
import librosa.display
from pyaudio import PyAudio, paInt16
from scipy.fftpack import fft,ifft
import matplotlib.pyplot as plt
import wave
import numpy as np

class Audio:
    __sr=0
    __y=None
    __tmp=None
    __doubleTracks=False

    def __init__(self,direction=None,_y=None,_sr=None,name=None):
        if direction!=None:
            y,r=librosa.load(direction)
            self.__y=y
            self.__sr=r
            self.__tmp=direction
        if _sr!=None and name!=None:
            self.__y=np.real(_y)
            self.__sr=_sr
            self.__tmp=name
            librosa.output.write_wav(name,np.ascontiguousarray(np.real(_y)),_sr)
        if len(self.__y.shape)==2:
            self.__doubleTracks=True
        else:
            self.__doubleTracks=False

    def sound(self):
        wf=wave.open(self.__tmp,'rb')
        p=PyAudio()
        stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
        wf.getnchannels(),rate=wf.getframerate(),output=True)
        while True:
            data=wf.readframes(1024)
            if data=="":break
            stream.write(data)
        stream.close()
        p.terminate()

    def resample(self,newRate,name):
        return Audio(_y=librosa.resample(self.__y,self.__sr,newRate),_sr=newRate,name=name)
    
    def toOneTrack(self,track,name):
        return Audio(_y=self.__y[track],_sr=self.__sr,name=name)
    
    def select(self,name,start=None,end=None):
        if start==None:
            start=0
        if end==None:
            if self.__doubleTracks:
                end=self.__y.shape[1]
            else:
                end=self.__y.shape[0]
        return Audio(_y=self.__y[start:end],_sr=self.__sr,name=name)
    
    def getLength(self):
        if self.__doubleTracks:
            return self.__y.shape[1]
        else:
            return self.__y.shape[0]

    def plot(self,axes=None,axes1=None):
        if self.__doubleTracks:
            end=self.__y.shape[1]
            x=np.arange(0,end/self.__sr,1/self.__sr)
            y1=self.__y[0]
            y2=self.__y[1]
            if axes==None:
                plt.figure()
                plt.subplot(2,1,1,xlabel="t/s",ylabel="amplitude").plot(x,y1)
                plt.subplot(2,1,2,xlabel="t/2",ylabel="amplitude").plot(x,y2)
                plt.show()
            else:
                axes.plot(x,y1)
                if axes1!=None:
                    plt.xlabel("t/s")
                    plt.ylabel("amplitude")
                    plt.plot(x,y2)
                    plt.show()
        else:
            end=self.__y.shape[0]
            x=np.arange(0,end/self.__sr,1/self.__sr)
            y=self.__y
            if axes==None:
                plt.xlabel("t/s")
                plt.ylabel("amplitude")
                plt.plot(x,y)
                plt.show()
            else:
                axes.plot(x,y)

    def FFT(self):
        if not self.__doubleTracks:
            sr=self.__sr
            tfLength=self.__y.shape[0]
            return AudioFrequency(np.arange(0,sr,sr/tfLength),fft(self.__y),self.__sr)
        else:
            sr=self.__sr
            tfLength=self.__y.shape[1]
            return AudioFrequency(np.arange(0,sr,sr/tfLength),fft(self.__y[0]),self.__sr),AudioFrequency(np.arange(0,sr,sr/tfLength),fft(self.__y[1]),self.__sr)
    
    def __getF(self,y,maxf,tfStart=0,tfLength=None,tfTime=None):
        sr=self.__sr
        if tfTime!=None:
            tfLength=tfTime*sr
        elif tfLength==None:
            tfLength=y.shape[0]
        maxPoint=int(np.ceil(maxf/sr*tfLength))
        return np.arange(0,maxf,sr/tfLength),2*np.abs(fft(y[tfStart:tfStart+tfLength])[:maxPoint])
    
    def stft(self,points):
        if not self.__doubleTracks:
            duration=librosa.get_duration(filename=self.__tmp)
            sr=self.__sr
            step=int(duration*sr/points)
            plt.ion()
            for start in range(0,1024*step,step):
                fx,fy=self.__getF(self.__y,sr,start,step)
                plt.xlabel("frequency/Hz")
                plt.ylabel("amplitude")
                plt.title("{0}s".format(start*duration/1024/step))
                plt.plot(fx[:int(len(fx)/2)],fy[:int(len(fx)/2)])
                plt.pause(0.005)
                plt.clf()

class AudioFrequency:
    __f=None
    __x=None
    __sr=0

    def __init__(self,x,y,sr):
        self.__x=x
        self.__f=y
        self.__sr=sr

    def plot(self,maxf=None,axes=None):
        if maxf==None:
            maxf=int(self.__sr/2)
        maxPoint=int(np.ceil(maxf/self.__sr*(self.__x.shape[0])))
        if axes==None:
            plt.xlabel("frequency/Hz")
            plt.ylabel("amplitude")
            plt.plot(self.__x[:maxPoint],2*np.abs(self.__f)[:maxPoint])
            plt.show()
        else:
            axes.plot(self.__x[:maxPoint],2*np.abs(self.__f)[:maxPoint])
        
    def IFFT(self,name):
        return Audio(_y=ifft(self.__f),_sr=self.__sr,name=name)

    def getMaxFrequency(self):
        return np.argmax(2*np.abs(self.__f))*(self.__sr/self.__f.shape[0]),2*np.abs(self.__f[np.argmax(2*np.abs(self.__f))])/self.__f.shape[0]


def get_audio(filepath,sr,RECORD_SECONDS):
    def save_wave_file(pa, filename, data,sr):
        '''save the date to the wavfile'''
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        # wf.setsampwidth(sampwidth)
        wf.setsampwidth(pa.get_sample_size(paInt16))
        wf.setframerate(sr)
        wf.writeframes(b"".join(data))
        wf.close()
    isstart = str(input("是否开始录音？ （1/0）")) #输出提示文本，input接收一个值,转为str，赋值给aa
    if isstart == str("1"):
        pa = PyAudio()
        stream = pa.open(format=paInt16,
                         channels=1,
                         rate=sr,
                         input=True,
                         frames_per_buffer=1024)
        print("*" * 10, "开始录音：请在"+str(RECORD_SECONDS)+"秒内输入语音")
        frames = []  # 定义一个列表
        for i in range(0, int(sr / 1024 * RECORD_SECONDS)):  # 循环，采样率 44100 / 1024 * 5
            data = stream.read(1024)  # 读取chunk个字节 保存到data中
            frames.append(data)  # 向列表frames中添加数据data
        print("*" * 10, "录音结束\n")
 
        stream.stop_stream()
        stream.close()  # 关闭
        pa.terminate()  # 终结
 
        save_wave_file(pa, filepath, frames,sr)
    elif isstart == str("0"):
        exit()
    else:
        print("无效输入，请重新选择")
        get_audio(filepath,sr,RECORD_SECONDS)
    return Audio(filepath)
