'''
Script to analyze the litoralis songs recorded in speaker - mic setup
(For now it only creates all the wav-files)

authors: Eric, Adrian, Tjasa, Felicia
'''

###############################################################################
## imports
###############################################################################

import numpy as np
# get DataLoader from https://github.com/relacs/pyrelacs
import DataLoader as dl
# get audioio from https://github.com/bendalab/audioio
import audioio as ai
import glob
import os
import matplotlib.pyplot as plt
import scipy.signal as sig

###############################################################################
## functions
###############################################################################

def create_filename(directory, num=1) :
    """
    creates basic name for a file containing condition and distance information.
    Use num to assign numbers if more than one file per distance will be created
    """
    file = directory + '/info.dat'
    info = dl.load(file)[0]
    distancestr = info['Distance']
    conditionstr= info['Condition']
    speciesName = 'Pholidoptera_littoralis_'
    return speciesName+conditionstr+'_'+distancestr+'_'+str(num)

def bandpass_filter(data, rate, lowf=2000.0, highf=20000.0):
    """
    Bandpass filter the signal.
    """
    nyq = 0.5*rate
    low = lowf/nyq
    high = highf/nyq
    b, a = sig.butter(4, [low, high], btype='bandpass')
    fdata = sig.lfilter(b, a, data)
    return fdata

###############################################################################
## main script
###############################################################################

# set working directory
#os.chdir("/home/felicia/Dokumente/01 - Uni/01-SS16/Sensory Systems in Natural Environments/Data/DistanceMeadow/")

# get all distance conditions
directories = sorted(glob.glob('2016-07-21-*-meadow'))

for dir in directories :

    file = dir + '/stimulus-file-traces.dat'
    counter = 1

    for info, key, data in dl.iload(file) :

        time = data[:,0]
        intensity = data[:,1] #TODO is intensity correct?

        #TODO: rate is...
        rate = np.round(1000.0/np.mean(np.diff(time)))
        #TODO: wave is...
        wave = bandpass_filter(intensity - np.mean(intensity), rate)

        # maximal amplitude (may be positive or negative)
        maxampl = np.max(np.abs(wave))
        # normalize wave to [-1,1]
        nwave = wave/maxampl

        # create telling name
        name = create_filename(dir, counter)

        # create the wav file
        ai.write_audio(name+'.wav', nwave, rate)

        #plt.plot(wave/maxampl)
        #plt.show()

        counter = counter + 1
        
        # try stuff to make FFT
        ps = np.abs(np.fft.fft(wave))**2
        time_step = np.mean(np.diff(time)) 
        freqs = np.fft.fftfreq(wave.size, time_step)
        freqs = np.abs(freqs)
        idx = np.argsort(freqs)
        plt.plot(freqs[idx], ps[idx])
        plt.show()
