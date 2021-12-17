import pyaudio
import wave
import cv2
import os
import pickle
import time
import sys
from scipy.io.wavfile import read
from IPython.display import Audio, display, clear_output

from common import *

FILENAME = './temp.wav'

def recognize(filename=FILENAME):
    #read test file
    sr, audio = read(filename)

    gmm_files = [os.path.join(PATH_MODEL,fname) for fname in 
                os.listdir(PATH_MODEL) if fname.endswith('.gmm')]

    models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
                in gmm_files]

    # extract mfcc features
    vector = extract_features(audio,sr)
    log_likelihood = np.zeros(len(models)) 

    #checking with each model one by one
    for i in range(len(models)):
        gmm = models[i]         
        scores = np.array(gmm.score(vector))
        log_likelihood[i] = scores.sum()
    
    pred = np.argmax(log_likelihood)
    identity = speakers[pred]
   
    # if voice not recognized than terminate the process
    if identity == 'unknown':
            print("Not Recognized! Try again...")
            return identity
    
    print( "Recognized as - ", identity)
    return identity

def recognize_from_console():
    # Voice Authentication
    
    # FILENAME = "./test.wav"

    audio = pyaudio.PyAudio()
   
    # start Recording
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

    time.sleep(2.0)
    print("recording...")
    frames = []

    for i in range(0, int(RATE / CHUNK * REGCOGNIZE_RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("finished recording")


    # stop Recording
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # saving wav file 
    waveFile = wave.open(FILENAME, 'wb')
    waveFile.setnchannels(CHANNELS)
    waveFile.setsampwidth(audio.get_sample_size(FORMAT))
    waveFile.setframerate(RATE)
    waveFile.writeframes(b''.join(frames))
    waveFile.close()

    # gmm_files = [os.path.join(PATH_MODEL,fname) for fname in 
    #             os.listdir(PATH_MODEL) if fname.endswith('.gmm')]

    # models    = [pickle.load(open(fname,'rb')) for fname in gmm_files]

    # speakers   = [fname.split("/")[-1].split(".gmm")[0] for fname 
    #             in gmm_files]
  
    # if len(models) == 0:
    #     print("No Users in the Database!")
    #     return
    
    recognize()
    
if __name__ == '__main__':
    if len(sys.argv) == 1:
        recognize_from_console()
    if len(sys.argv) == 2:
        FILENAME = sys.argv[1]
        padding(FILENAME, REGCOGNIZE_RECORD_SECONDS)
        recognize()
    else:
        print('wrong syntax')