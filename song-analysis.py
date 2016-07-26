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

# get all distance conditions
directories = sorted(glob.glob('2016-07-23-*-bush'))
all_data_8kHz = []
data_dict = defaultdict(list)


for dir in directories :

    file = dir + '/stimulus-rectangular-traces.dat'
    counter = 1
    
    #first all the 8kHz signals are extracted, then you must manually changed prev_carrier to 15kHz
    #also change the all_data_* list, and switch which sections are commented/uncommented underneath that
    prev_carrier = '8kHz'
    for info, key, data in dl.iload(file) :
        
        carrier_freq = info[0]['carrierfreq']
        
        if prev_carrier == carrier_freq:
            
        
            carrier_freq = float(carrier_freq.replace('kHz',''))
    
            #get variables for list of total data
            name, distancestr, conditionstr = create_filename(dir, counter)
            time = data[:,0]
            intensity = data[:,1] #TODO is intensity correct?
            distancestr = float(distancestr.replace('cm',''))
           
            
            #TODO: rate is...
            rate = np.round(1000.0/np.mean(np.diff(time)))
            #TODO: wave is...
            wave = bandpass_filter(intensity - np.mean(intensity), rate)
            stdWave = np.std(wave, ddof=1)
            # maximal amplitude (may be positive or negative)
            maxampl = np.max(np.abs(wave))
            # normalize wave to [-1,1]
            nwave = wave/maxampl
    
            # create the wav file
            #ai.write_audio(name+'.wav', nwave, rate)
            
            #plt.plot(wave)
            #plt.show()
    
            counter = counter + 1
        
            # try stuff to make FFT
            ps = np.abs(np.fft.fft(wave))**2
            time_step = np.mean(np.diff(time))
            freqs = np.fft.fftfreq(wave.size, time_step)
            freqs = np.abs(freqs)
            idx = np.argsort(freqs)
            #plt.figure()
            #plt.plot(freqs[idx], ps[idx])
            #plt.show()
            """
            data_dict['environment'].append(conditionstr) 
            data_dict['distance'].append(distancestr)
            data_dict['carrierFrequency'].append( carrier_freq)
            data_dict ['wave'].append( wave)
            data_dict ['stdWave'].append(stdWave)
            data_dict ['time'].append(time)
            data_dict ['FFTfreqs'].append(freqs)
            data_dict ['FFTps'].append( ps)
            data_dict ['FFTidx'].append(idx)
            """
            #save important variables into a list
            all_data_8kHz.append([conditionstr, distancestr, carrier_freq, stdWave])#, stdWave, time])
        else:
            continue

"""
#make these variables stuff to work with
all_data_15 = np.array(all_data_15kHz)
distanceMeadow15 = np.asarray(all_data_15[:,1], dtype=float)
stdWave15 = np.asarray(all_data_15[:,3], dtype=float)
avg_std15 = np.array([np.mean(stdWave15[s_ind:s_ind+4]) for s_ind in np.arange(0, len(stdWave15), 5)])
std_std15 = np.array([np.std(stdWave15[s_ind:s_ind+4], ddof=1) for s_ind in np.arange(0, len(stdWave15), 5)])

avg_distance15 = np.array([np.mean(distanceMeadow15[s_ind:s_ind+4]) for s_ind in np.arange(0, len(distanceMeadow15), 5)])
"""

all_data_8 = np.array(all_data_8kHz)
distanceMeadow8 = np.asarray(all_data_8[:,1], dtype=float)
stdWave8 = np.asarray(all_data_8[:,3], dtype=float)
avg_std8 = np.array([np.mean(stdWave8[s_ind:s_ind+4]) for s_ind in np.arange(0, len(stdWave8), 5)])
std_std8 = np.array([np.std(stdWave8[s_ind:s_ind+4], ddof=1) for s_ind in np.arange(0, len(stdWave8), 5)])

avg_distance8 = np.array([np.mean(distanceMeadow8[s_ind:s_ind+4]) for s_ind in np.arange(0, len(distanceMeadow8), 5)])

"""
plt.loglog(avg_distance15, avg_std15, '*', color='red', ms=10)
#plt.fill_between(avg_distance15, y1=avg_std15+std_std15, y2=avg_std15-std_std15, color='red', alpha=0.6)
plt.loglog(avg_distance8, avg_std8, 'o', color='blue', ms=10)
#plt.fill_between(avg_distance8, y1=avg_std8+std_std8, y2=avg_std8-std_std8, color='blue', alpha=0.6)

plt.title('loglog: Distance vs. SD in Bushes')
plt.xlabel('Distance')
plt.ylabel('SD')
plt.show()
"""
