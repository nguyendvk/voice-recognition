from sklearn import preprocessing
import python_speech_features as mfcc
import numpy as np
import os
import pyaudio
import librosa
from pydub import AudioSegment
import warnings
from shutil import copyfile

warnings.filterwarnings("ignore")
PATH_DB = './voice_database'
PATH_MODEL = './models'
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
REGCOGNIZE_RECORD_SECONDS = 4
REGISTER_RECORD_SECONDS = 3


def padding(filename, sec):
    pad_ms = int((sec - librosa.get_duration(filename=filename)) * 500) #ms
    if pad_ms == 0:
        return
    silence = AudioSegment.silent(duration=pad_ms)
    audio = AudioSegment.from_wav(filename)

    padded = silence + audio + silence  # Adding silence after the audio
    padded.export(filename, format='wav')

def extract_features(audio,rate):    
    # mfcc(signal, rate, winlen, winstep )
    mfcc_feat = mfcc.mfcc(audio,rate, 0.025, 0.01,20,appendEnergy = True, nfft=1103)
    mfcc_feat = preprocessing.scale(mfcc_feat)
    delta = calculate_delta(mfcc_feat)

    #combining both mfcc features and delta
    combined = np.hstack((mfcc_feat,delta)) 
    return combined

def calculate_delta(array):
    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
                first = 0
            else:
                first = i-j
            if i+j > rows -1:
                second = rows -1
            else:
                second = i+j
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def init():
    if not os.path.exists(PATH_DB):
        os.makedirs(PATH_DB)
    if not os.path.exists(PATH_MODEL):
        os.makedirs(PATH_MODEL)
    if not os.path.isfile(os.path.join(PATH_MODEL, 'unknown.gmm')):
        copyfile('./unknown.gmm', os.path.join(PATH_MODEL,'unknown.gmm'))