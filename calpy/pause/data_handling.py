from .. import dsp
from .. import plots
from ..utilities import read_wavfile
from ..entropy import symbolise_speech, entropy_profile
import numpy as np
import json
import matplotlib.pyplot as plt


def get_pause_digitized(file_name, min_silence=0.0001):
    '''Used in audio_file_.compute_pauses_from_audio'''   
    #get the array of [0,1,0,.....,1,1,1]
        #where 1's = pause (taken from entropy.symbolise_pauses)
    fs, sound = read_wavfile(file_name)
    pause = dsp.pause_profile(sound, fs, min_silence) #pauses counted in units of 1ms
    pitch = dsp.pitch_profile(sound, fs)
    prosody = np.append([pitch], [pause], axis=0)
    symbols = np.array([])
    for arr in np.array_split(prosody, pause.shape[0] // 10, axis=1):
        symbols = np.append(symbols, symbolise_speech(arr[0,:], arr[1,:]))
    return symbols 

def get_pause_frequencies(symbols):
    '''Used in audio_file_.compute_pauses_from_audio'''   
    pause = 0
    pause_times = []
    current_pause_count = 0
    previously_pausing = False
    for symbol in symbols:
        #pause either just starting or continuing
        if symbol == pause: 
            current_pause_count += 1
            if not previously_pausing:
                previously_pausing = True
        #uptake in talking or still talking
        else: 
            if previously_pausing: 
                previously_pausing = False #pause_array has ended
                pause_times.append(current_pause_count)
                current_pause_count = 0
            else:
                continue
    return pause_times

def get_pause_frequencies_to_dictionary(symbols):
    """Old code
    """
    #write array to file
    '''write_to_file("probabilities_output.txt", symbols)'''
    #look for series of unbroken pauses in array
    pause = 0 #dsp.pause_profile returns 1 marking sound
    pause_time_freq = {}
    current_pause_count = 0
    currently_pausing = False 
    for elem in symbols:
        #pause either just starting or continuing
        if elem == pause: 
            if currently_pausing:
                current_pause_count += 1
            else:
                current_pause_count = 1
                currently_pausing = True
        #uptake in talking or still talking
        else: 
            if currently_pausing: 
                currently_pausing = False #pause_array has ended
                #record freq to nearest 10
                #Reducing down to lots of 10
                '''current_one_count = current_one_count - (current_one_count%10)'''
                #check if freq exists in dictionary already (dont want to overwrite)
                if current_pause_count in pause_time_freq:
                    #grab key with matching freq
                    #take value out, add 1, then put back in
                    old_freq = pause_time_freq[current_pause_count]
                    new_freq = old_freq + 1
                    pause_time_freq[current_pause_count] = new_freq
                else:
                    pause_time_freq[current_pause_count] = 1
            else:
                continue
    return pause_time_freq
    

    #print values
    '''for key in sorted(pause_time_freq.keys()):'''
    #   '''print("%s: %s" % (key, pause_time_freq[key]))'''
    #write print values to file
    '''write_dict_to_file("pause_freq_dist.txt", pause_time_freq)'''
    #print(pause_time_freq.keys())
    #print(pause_time_freq.values())
    #plt.bar(pause_time_freq.keys(), pause_time_freq.values())
    #histogram(pause_time_freq)

def write_distribution(file_name):
    """Old code

        Desc:

    """
    fs, sound = read_wavfile(file_name)
    pause = dsp.pause_profile(sound, fs)
    pitch = dsp.pitch_profile(sound, fs)
    prosody = np.append([pitch], [pause], axis=0)
    symbols = np.array([])
    for arr in np.array_split(prosody, pause.shape[0] // 10, axis=1):
        symbols = np.append(symbols, symbolise_speech(arr[0,:], arr[1,:]))
    print(symbols[3])
    #file = open("symbols_01.txt","w")
    #symbols_str = ''.join(symbols[:])
    #file.write(symbols_str)
    #np.histogram(symbols, bins=[0,1])






    