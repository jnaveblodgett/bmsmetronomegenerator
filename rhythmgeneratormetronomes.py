# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 17:25:37 2017

@author: Jessica
"""

#part 1: making an all-low-beep subdivision metronome

import scipy.io.wavfile as wav
import pandas as pd # install with "pip install pandas" on the command line
import numpy as np

musicname = "vivaespana_BMSNEAMEEG.wav"
csvname = "BMSNEAMEEG_vivaespana_subdivision.csv"
outputfilenames = ["vivaespana_subdivision_alllow_BMSNEAMEEG.wav","vivaespana_subdivision_highlow_on1_BMSNEAMEEG.wav","vivaespana_subdivision_highlow_on2_BMSNEAMEEG.wav","vivaespana_rhythm_alllow_BMSNEAMEEG.wav","vivaespana_rhythm_highlow_BMSNEAMEEG.wav"]

beep_length = 0.01
high_pitch = 523
low_pitch = 261

maqsoum_all = [1,2,4,5,7]
maqsoum_doum = [1,4,5]
maqsoum_tek = [2,7]


events = pd.read_csv(csvname, header=None)
sample_rate, music = wav.read(musicname)

beep_times = events[0]
high_beeps = events[1] == 1
 
t = np.linspace(0,beep_length,beep_length*sample_rate) # create a half second sound (for our metronome click)
low = np.sin(2*np.pi*low_pitch * t)*0.5 # create a lower-pitched sine wave beep).
high = np.sin(2*np.pi*high_pitch * t)*0.7 # create a higher-pitched sine wave beep).

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
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(low),low]).T
    else:
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(low),low]).T


wav.write(outputfilenames[0],sample_rate,music)

#then make the high-low metronome on 1

events = pd.read_csv(csvname, header=None)
sample_rate, music = wav.read(musicname)

beep_times = events[0]
#high_beeps = events[1] == 1 and events[1] == 3 and events[1] == 5 and events[1] == 7
#high_beeps = events[1] == 1 and 3 and 5 and 7
high_beeps = events[1] % 2 == 1


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


wav.write(outputfilenames[1],sample_rate,music)

#then make the high-low metronome on 2

events = pd.read_csv(csvname, header=None)
sample_rate, music = wav.read(musicname)

beep_times = events[0]
high_beeps = events[1] % 2 == 0


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


wav.write(outputfilenames[2],sample_rate,music)


#then the all-low rhythm

events = pd.read_csv(csvname, header=None)
sample_rate, music = wav.read(musicname)

def myfilter(arg):
  goodvals = [1, 2, 4, 5, 7]
  return arg in goodvals

beep_times = events[0]
high_beeps = events[1].map(myfilter)
#high_beeps = events[1] == any(maqsoum_all)
#high_beeps = events[1] == 1 | events[1] == 2 | events[1] == 4 | events[1] == 5 | events[1] == 7

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
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(low),low]).T
    else:
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")]


wav.write(outputfilenames[3],sample_rate,music)

#then the high-low doum-tek rhythm
events = pd.read_csv(csvname, header=None)
sample_rate, music = wav.read(musicname)

def lowfilter(arg):
  goodvals = [1, 4, 5, ]
  return arg in goodvals

def highfilter(arg):
  goodvals = [2, 7]
  return arg in goodvals

beep_times = events[0]
high_beeps = events[1].map(highfilter)
low_beeps = events[1].map(lowfilter)

t = np.linspace(0,beep_length,beep_length*sample_rate) # create a half second sound (for our metronome click)
low = np.sin(2*np.pi*low_pitch * t)*0.5 # create a 830Hz sine wave beep).
high = np.sin(2*np.pi*high_pitch * t)*0.7 # create a 1661Hz sine wave beep).

low = np.minimum(2**15, np.maximum(-2**15+1, low * 2**15)).astype("int16")
high = np.minimum(2**15, np.maximum(-2**15+1, high * 2**15)).astype("int16")

#music = np.minimum(2**15, np.maximum(-2**15+1, music * 2**15)).astype("int16")

music = np.vstack([music,np.zeros_like(music)]).T


for t,is_high_beep,is_low_beep in zip(beep_times,high_beeps,low_beeps):
    #print(t)
    #print(is_low_beep)
    #print(np.round(t * sample_rate).astype("int_"))
    #break 
    if is_high_beep:
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(high),high]).T
    if is_low_beep:
        music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")] += np.vstack([np.zeros_like(low),low]).T
    else:
       music[np.round(t * sample_rate).astype("int_") : np.round(t*sample_rate + beep_length*sample_rate).astype("int_")]


wav.write(outputfilenames[4],sample_rate,music)
