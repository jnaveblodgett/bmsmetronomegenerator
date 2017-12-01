"""
created by David Little and Jessica Nave-Blodgett in 2016
but mostly by David Little (fr srs)

Automatic metronome generator that reads in .csv files that have timepoints and then generates tones based on the timing locations in the stuff

"""

import scipy.io.wavfile as wav
import pandas as pd # install with "pip install pandas" on the command line
import numpy as np


events = pd.read_csv("newyork_bsma.csv", header=None)
sample_rate, music = wav.read("newyork.wav")

beep_times = events[0]
high_beeps = events[1] == 1

beep_length = 0.01
high_pitch = 1661
low_pitch = 830
 
t = np.linspace(0,beep_length,beep_length*sample_rate) # create a half second sound (for our metronome click)
low = np.sin(2*np.pi*low_pitch * t)*0.5 # create a 830Hz sine wave beep).
high = np.sin(2*np.pi*high_pitch * t)*0.7 # create a 1661Hz sine wave beep).

low = np.minimum(2**15, np.maximum(-2**15+1, low * 2**15)).astype("int16")
high = np.minimum(2**15, np.maximum(-2**15+1, high * 2**15)).astype("int16")

#music = np.minimum(2**15, np.maximum(-2**15+1, music * 2**15)).astype("int16")

music = np.vstack([music,np.zeros_like(music)]).T


for t,is_high_beep in zip(beep_times,high_beeps):
    #print(t)
    #print(is_low_beep)
    #print(np.round(t * sample_rate).astype("int_"))
    #break 
    if is_high_beep:
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(high),high]).T
    else:
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(low),low]).T


wav.write("newyork_bsma.wav",sample_rate,music)
