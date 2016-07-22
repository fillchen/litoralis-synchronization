#TODO description
'''
Script to analyze ...
authors: Eric, Adrian, Tjasa, Felicia
'''


###############################################################################
## imports
###############################################################################

import numpy as np
import matplotlib.pyplot as plt
import os
import glob
# get DataLoader from https://github.com/relacs/pyrelacs
import DataLoader as dl

###############################################################################
## functions
###############################################################################

def get_distance(directory) :
    '''returns the distance in m'''
    file = directory + '/info.dat'
    info = dl.load(file)[0]
    distancestr = info['Distance']
    distance = 0.01*float(distancestr.replace('cm',''))
    return distance

def gain_vs_frequency(filename) :
    dat = np.loadtxt(fname=filename)
    x = dat[:,0]
    y = dat[:,1]
    ylabel = "gain"
    return x, y, ylabel

def exclude_pure_distance_effects(gain, distance) :
    ''' eliminates effects due to the general decrease of sound pressure with the distance
    -- https://en.wikipedia.org/wiki/Inverse-square_law#Acoustics
    -- sound pressure ~ 1/distance
    '''
    g = distance*gain
    ylabel = "gain*distance" #TODO find better name
    return g, ylabel

###############################################################################
## main script
###############################################################################

# set working directory
#os.chdir("/home/felicia/Dokumente/01 - Uni/01-SS16/Sensory Systems in Natural Environments/Data/DistanceMeadow/")

# get reference recordings (distance 100cm)
_ , reference_gain, _ = gain_vs_frequency('2016-07-22-aa-open/transferfunction-data.dat')

counter = 1
for dir in sorted(glob.glob('2016-07-22-*-open')) :

    # get path and general information
    file = dir + '/transferfunction-data.dat'
    distance = get_distance(dir)

    # construct subplot structure
    ax = plt.subplot(4,5,counter) #TODO adapt

    # values for frequency and gain (untransformed)
    freq, gain, ylabel = gain_vs_frequency(file)
    # normalize gain
    gain = gain/reference_gain
    # eliminate pure distance effects
    gain, ylabel = exclude_pure_distance_effects(gain,distance)
    # go to logarithmic scale
    gain = np.log10(gain)
    ylabel = "log " + ylabel
    # set the title
    title = distance #TODO title finding
    # plot
    ax.plot(freq/1000, gain) #create kHz
    ax.set_title(title)
    ax.set_xlabel("frequency [kHz]")
    ax.set_ylabel(ylabel)
    # adapt the limits
    ax.set_xlim(5,20)
    ax.set_ylim(-3,0)
    #plt.setp(ax,xticks=[6000,8000,10000,12000,14000,16000,18000,20000]) #simply to give info how to do ticks
    #plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0)) #simply to give info how to force scientific notation
    # counter needed for handle the subplots
    counter = counter + 1

# show all the plots, and make them pretty
# this adjusts the plots in the figure window (Left/Bottom/Right/Top/WidthSpace/HeightSpace
plt.subplots_adjust(.05,.05,.95,.95,.3, .55) 
plt.show()

#TODO : title, several graphs in one plot, beautify, rename
