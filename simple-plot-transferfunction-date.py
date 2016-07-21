import numpy as np
import matplotlib.pyplot as plt
import os
import glob
import DataLoader as dl

#os.chdir("/home/felicia/Dokumente/01 - Uni/01-SS16/Sensory Systems in Natural Environments/Data/DistanceMeadow/")

aa = np.loadtxt(fname='2016-07-21-aa-meadow/transferfunction-data.dat')

c = 1
for dir in sorted(glob.glob('2016-07-21-*-meadow')) :
    info = dl.load(dir + '/info.dat')[0]
    distancestr = info['Distance']
    distance = 0.01*float(distancestr.replace('cm',''))
    file = dir + '/transferfunction-data.dat'
    dat = np.loadtxt(fname=file)
    ax = plt.subplot(3,4,c)
    x = dat[:,0]
    y = dat[:,1]/aa[:,1]
    ytdist = distance*y
    ytdistlog = np.log10(ytdist)
    ax.plot(x,ytdistlog)
    ax.set_xlabel("frequency [Hz]")
    ax.set_ylabel("gain")
    ax.set_xlim(2000, 20000)
    ax.set_ylim(-3,0)
    ax.set_title(dir)
    c = c + 1
plt.show()
