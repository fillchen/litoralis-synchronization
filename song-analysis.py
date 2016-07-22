import numpy as np
import DataLoader as dl
import audioio as ai
import sys

# change dir

#print sys.path
#exit()

dat = '2016-07-21-ac-meadow/stimulus-file-traces.dat'

for info, key, data in dl.iload(dat) :
    print data.shape
    print info[0]['stimfile']
    rate = np.round(1000.0/np.mean(np.diff(data[:,0])))
    wave = data[:,1] - np.mean(data[:,1])
    maxampl = np.max(np.abs(wave))
    ai.write_audio('test.wav', wave/maxampl, rate)
    break
