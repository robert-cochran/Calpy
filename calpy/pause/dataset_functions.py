import numpy as np

from calpy.plots import plots
from calpy.pause import parameters
from calpy.pause import audio_file_
from calpy.pause import file_handling
from calpy.pause.dataset_folder import test

#swarmplot
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

#raincloud plot
import ptitprince as pt

#timer
import time

#---FUNCTIONS---
def pause_process_single_file(folder_dir, file_number, file_frequency):
    audio_file = audio_file_.AudioFile(folder_dir, file_number, file_frequency, parameters.min_silence, parameters.compute, parameters.printing)
    audio_file.pause_digitisation(parameters.compute)
    audio_file.symbolize(parameters.symbol_model)
    audio_file.entropy(parameters.selected_symbol, parameters.M, parameters.ap, parameters.bp, parameters.cp, parameters.window_size, parameters.window_overlap)
    audio_file.plots(parameters.bins, parameters.bin_range)
    return audio_file

def pause_process_test(folder_dir, file_number, file_frequency):
    # folder_dir = '/monologue/OSR/Male/'
    # file_number = 'OSR_us_000_0030'
    # file_frequency = '8000'
    test = pause_process_single_file(folder_dir, file_number, file_frequency)
    return test
    
def pause_process_dataset(folder_dir, file_numbers, file_frequency):
    audio_files = []
    for file_number in file_numbers:
        print(file_number)
        audio_files.append(pause_process_single_file(folder_dir, file_number, file_frequency))
    return audio_files

def pause_means(audio_files):
    '''Compute means and shit for histogram'''
    #pauses_all = []
    pauses_avg = []
    for audio_file in audio_files:
        #pauses_all.append(audio_file.pauses)
        #for pause in audio_file.pauses:
           # pauses_all.append(pause)
        avg = np.mean(audio_file.pauses)
        print(avg)
        print("file number: " + str(audio_file.file_number) + " number of pauses: " + str(audio_file.number_of_pauses))
        pauses_avg.append(avg)

        #avg_pause_length_all.append(avg)
        #print(str(file_number.file_number) + " : " + str(avg))
        #print("var : " + str(np.var(file_number.entropy_profile)))
    return pauses_avg

def averages(directory, audio_files):
    total_binary_pause_array_length = 0
    total_audio_pause = 0
    total_sounding = 0
    total_pause_proportion = 0
    total_number_of_pauses = 0
    total_avg_pause_length = 0

    for audio_file in audio_files:
        total_binary_pause_array_length = total_binary_pause_array_length + audio_file.binary_length
        total_audio_pause = total_audio_pause + audio_file.total_pauses
        total_sounding = total_sounding + audio_file.total_sounding
        total_pause_proportion = total_pause_proportion + audio_file.pause_proportion
        total_number_of_pauses = total_number_of_pauses + audio_file.number_of_pauses
        total_avg_pause_length = total_avg_pause_length + audio_file.average_pause_length


    avg_binary_pause_array_length = total_binary_pause_array_length/len(audio_files)
    avg_audio_pause = total_audio_pause/len(audio_files)
    avg_sounding = total_sounding/len(audio_files)
    avg_pause_proprtion = total_pause_proportion/len(audio_files)
    avg_number_of_pauses = total_number_of_pauses/len(audio_files)
    avg_pause_length = total_avg_pause_length/len(audio_files)

    file_handling.write_pause_averages(
                                        directory, 
                                        avg_binary_pause_array_length,
                                        avg_audio_pause,
                                        avg_sounding,
                                        avg_pause_proprtion,
                                        avg_number_of_pauses,
                                        avg_pause_length
                                        )


def resolution_tests():
    folder_dir = '/resolution-experiments/'
    file_number = '6269'
    file_frequency_all = ['11025', '16000', '22050', '32000', '44100', '48000', '88200', '96000']
    audio_files = []
    for file_frequency in file_frequency_all:
        start = time.time()
        print(file_frequency)
        audio_files.append(pause_process_single_file(folder_dir, file_number, file_frequency))
        end = time.time()
        timer = end-start
        print("minutes: " + str(timer/60) + "   seconds: " + str(timer))
    return audio_files

def raincloud_plot(folder_dir, file_name, x_data, title, y_label, x_label):


    sns.set(style="whitegrid")
    #ax = sns.boxplot(x=pauses, whis=np.inf)
    #ax = sns.swarmplot(x=pauses, color='black')

    #x = (3.5+2*np.random.randn(1000, 1))#); x1 = (-3.5+2*np.random.randn(1000, 2))
    #x=np.concatenate((x,x1),axis=0)
    #x_cat = np.random.randint(0,4,size=(2000, 1))
    #x=np.concatenate((x_cat,x),axis=1)
    #df_rand = pd.DataFrame(pauses, columns=['pauses','all pauses'])
    fig, ax = plt.subplots(figsize=(8,3))
    ax = pt.RainCloud(x=np.array(x_data),orient='h',bw=.1, ax=ax)
    #sns.despine()

    #sns.despine()
    #ax.figure.set_size_inches(12,8)
    plt.title(title)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    #ax.xlabel(x_label)
    #fig.xlabel(x_label)
    plt.savefig('./output' + folder_dir + file_name + '/' + 'raincloud_pause_groups_num_all.png')
    #plt.show()

def pause_code():
    #show poor and good audio files in pause code plot
    channel_A = './data/dialogue/conversations/media.talkbank.org/ca/CallHome/eng/1/4247/split_mono/4247_16000_A/4247_16000_A.wav'
    channel_B = './data/dialogue/conversations/media.talkbank.org/ca/CallHome/eng/1/4247/split_mono/4247_16000_B/4247_16000_B.wav'
    students.plot_sounding_pattern(channel_A, channel_B, parameters.min_silence, time_range=(0,1), xtickevery=0.5, row_width=5)

def symbol_averages(audio_files):
    a = 0
    b = 0
    c = 0
    d = 0
    e = 0
    f = 0
    g = 0
    h = 0
    i = 0
    j = 0

    for audio_file in audio_files:
        a = audio_file.symbol_occurrence[0] + a
        b = audio_file.symbol_occurrence[1] + b
        c = audio_file.symbol_occurrence[2] + c
        d = audio_file.symbol_occurrence[3] + d
        e = audio_file.symbol_occurrence[4] + e
        f = audio_file.symbol_occurrence[5] + f
        g = audio_file.symbol_occurrence[6] + g
        h = audio_file.symbol_occurrence[7] + h
        i = audio_file.symbol_occurrence[8] + i
        j = audio_file.symbol_occurrence[9] + j

    a = a/11
    b = b/11
    c = c/11
    d = d/11
    e = e/11
    f = f/11
    g = g/11
    h = h/11
    i = i/11
    j = j/11

    print(a)
    print(b)
    print(c)
    print(d)
    print(e)
    print(f)
    print(g)
    print(h)
    print(i)
    print(j)

def symbol_counts_check(audio_file):
    sum_prob = 0
    for i in range(10):
        sum_prob = sum_prob + audio_file.letter_probability[i] 
    print("sum prob from 1 to 10: " + str(sum_prob))
    print("sum(audio_file.letter_prob) for all: " + str(sum(audio_file.letter_probability)))
    
    sum_symbol_counts = 0
    for i in range(len(audio_file.ranked_probability)):
        sum_symbol_counts = sum_symbol_counts + audio_file.ranked_probability[i][0]
    print("sum_symbol_counts: " + str(sum_symbol_counts))
    print("total number of pauses: " + str(audio_file.number_of_pauses))
'''Plots'''
#plots.histogram_fn(jpn.directory, jpn.avgs_no_outliers_below_200, 25, (0,100), 'japanese')

#raincloud_plot(cf_eng_n, 'female_only', np.array(mean), 'Number of Pauses of each audio female only file', 'y label', 'x label')