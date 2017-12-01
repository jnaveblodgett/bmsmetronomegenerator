# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 12:36:58 2017

@author: Jessica
"""


import scipy.io.wavfile as wav
import pandas as pd # install with "pip install pandas" on the command line
import numpy as np

musicname = "Ziyan.wav"
csvname = ["Ziyan_BSMS.csv","Ziyan_BSMS2.csv","Ziyan_BSMS3_5.csv","Ziyan_BSMS4.csv","Ziyan_BSMA.csv","Ziyan_BAMS.csv","Ziyan_BAMA+3.csv","Ziyan_BAMA+4.csv","Ziyan_BAMA-3.csv","Ziyan_BAMA-4.csv","Ziyan_BAMA+3_15.csv","Ziyan_BAMA+4_15.csv","Ziyan_BAMA-3_15.csv","Ziyan_BAMA-4_15.csv","Ziyan_subdivision.csv"]
outputfilenames = ["Ziyan_BSMS_RAMP_SimpleTurkish.wav","Ziyan_BSMS2_RAMP_SimpleTurkish.wav","Ziyan_BSMS3_5_RAMP_SimpleTurkish.wav","Ziyan_BSMS4_RAMP_SimpleTurkish.wav","Ziyan_BSMA_RAMP_SimpleTurkish.wav","Ziyan_BAMS_RAMP_SimpleTurkish.wav","Ziyan_BAMA+3_RAMP_SimpleTurkish.wav","Ziyan_BAMA+4_RAMP_SimpleTurkish.wav","Ziyan_BAMA-3_RAMP_SimpleTurkish.wav","Ziyan_BAMA-4_RAMP_SimpleTurkish.wav","Ziyan_BAMA+3_15_RAMP_SimpleTurkish.wav","Ziyan_BAMA+4_15_RAMP_SimpleTurkish.wav","Ziyan_BAMA-3_15_RAMP_SimpleTurkish.wav","Ziyan_BAMA-4_15_RAMP_SimpleTurkish.wav","Ziyan_subdivision_RAMP_SimpleTurkish.wav"]

beep_length = 0.01
high_pitch = 1661
low_pitch = 830


#CSV number 1


for x in xrange(0,14):
    
    events = pd.read_csv(csvname[x], header=None)
    sample_rate, music = wav.read(musicname)

    beep_times = events[0]
    high_beeps = events[1] == 1
 
    t = np.linspace(0,beep_length,beep_length*sample_rate) # create a half second sound (for our metronome click)
    low = np.sin(2*np.pi*low_pitch * t)*0.5 + np.sin(3*2*np.pi*low_pitch * t)/3 + np.sin(5*2*np.pi*low_pitch * t)/5 + np.sin(7*2*np.pi*low_pitch * t)/7 + np.sin(9*2*np.pi*low_pitch * t)/9 + np.sin(11*2*np.pi*low_pitch * t)/11 + np.sin(13*2*np.pi*low_pitch * t)/13 # create a 830Hz sine wave beep).
    high = np.sin(2*np.pi*high_pitch * t)*0.7 + np.sin(3*2*np.pi*high_pitch * t)/3 + np.sin(5*2*np.pi*high_pitch * t)/5 + np.sin(7*2*np.pi*high_pitch * t)/7 + np.sin(9*2*np.pi*high_pitch * t)/9 + np.sin(11*2*np.pi*low_pitch * t)/11 + np.sin(13*2*np.pi*low_pitch * t)/13 # create a 1661Hz sine wave beep).

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

    wav.write(outputfilenames[x],sample_rate,music)
