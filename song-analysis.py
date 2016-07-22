import numpy as np
import DataLoader as dl
import audioio as ai
import glob
import os
import matplotlib.pyplot as plt
import scipy.signal as sig


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

# change dir
os.chdir("/home/felicia/Dokumente/01 - Uni/01-SS16/Sensory Systems in Natural Environments/Data/DistanceMeadow/")

for dir in sorted(glob.glob('2016-07-21-*-meadow')) :

    dat = dir + '/stimulus-file-traces.dat'

    for info, key, data in dl.iload(dat) :
        print data.shape
        print info[0]['stimfile']
        print key
        rate = np.round(1000.0/np.mean(np.diff(data[:,0])))
    #    wave = data[:,1] - np.mean(data[:,1])
        wave = bandpass_filter(data[:,1] - np.mean(data[:,1]), rate)
        maxampl = np.max(np.abs(wave))
        ai.write_audio(dir + '.wav', wave/maxampl, rate)
        plt.plot(wave/maxampl)
        plt.show()
        break

# get powerspectrum - mathplotlib.mlab psd()
#
