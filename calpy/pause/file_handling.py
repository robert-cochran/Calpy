import sys
import numpy
#import calpy
import calpy.dsp.audio_features as ca
import calpy.plots as cp
import calpy.utilities as cu
import calpy.pause as pause
import os
from pydub import AudioSegment
    #required a brew install ffmpeg

#-----File Settings---------
numpy.set_printoptions(threshold=sys.maxsize)

def create_folder(directory):
    """Creates a folder directory

    Given dir path, folders are created on disk. Wrong things may happen if 
    silly names are given as folder names

    Args:
        directory: the directory path that will be created on 
            disc

    Returns:
        Nothing, but the folders are created. For
        example:

        ./output/new_folder/second_folder

    Raises:
        IOError: Not sure if this error occurs or not
    """
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def write_binary_pause(audio_file):
    """ 
    """

    binary_pause_file = open("./output" + audio_file.folder_dir + "binary_pauses.txt", "w+")
    binary_pause_file.write(str(audio_file.binary_pauses).replace('.', ','))
    binary_pause_file.close()
    
    parameters_file = open("./output" + audio_file.folder_dir + "input_pause_parameters.txt", "w+")
    parameters_file.write(
                            "File \n "
                            "Input Audio File Directory: ./data" + audio_file.audio_file_path + "\n "
                            "Audio File Frequency: " + audio_file.file_frequency + "\n\n"
                            "Pause \n "
                            "Minimum Silence: " + str(audio_file.min_silence) + "\n\n"
                            )
    parameters_file.close()

def read_binary_pause(audio_file):
    """Reads an array from file

        Desc.
            All the audio files that are analysed for pauses have the raw pause outputs saved to file, 
                this reads those arrays back from a string into an array 

        Args:
            File Path: String
                The path after output, pause_frequency.txt will be concatenated at end

        Returns:
            an array properly formatted 

        Raises:
            --
    """


    #-----Binary Pause File------
    binary_pause_file = open("./output" + audio_file.folder_dir + "binary_pauses.txt", "r")
    binary_pause_read = binary_pause_file.read()
    binary_pause_read = binary_pause_read.strip('[').strip(']').replace(',', '').split(' ')
    audio_file.binary_pauses = []
    for audio_point in binary_pause_read:
        audio_file.binary_pauses.append(int(audio_point))
    binary_pause_file.close()

    # #-----Pause File------
    # pause_file = open("./output" + audio_file.folder_dir + "pauses.txt", "r")
    # pause_file_read = pause_file.read()
    # pause_file_read = pause_file_read.strip('[').strip(']').replace(',', '').split(' ')
    # audio_file.pauses = []
    # for pause in pause_file_read:
    #     audio_file.pauses.append(int(pause))
    # pause_file.close()

def write_pauses(audio_file):
    pause_file = open("./output" + audio_file.folder_dir + "pauses.txt", "w+")
    pause_file.write(str(audio_file.pauses))
    pause_file.close()

def write_pause_info(audio_file):
    data_file = open("./output" + audio_file.folder_dir + "output_data.txt", "w+")
    data_file.write("Time Stamp: " + audio_file.time_stamp + "\n\n"
                    "Pause \n "
                    "Binary_Pause_Total_Length(Audio_file_length): " + str(audio_file.binary_length) + "\n "
                    "Number_of_Pauses: " + str(audio_file.number_of_pauses) + "\n " 
                    "Total_Pauses: " + str(audio_file.total_pauses) + "\n "
                    "Total_Sounding: " + str(audio_file.total_sounding) + "\n "
                    "Pause_Proportion: " + str(audio_file.pause_proportion) + "\n "
                    "Average_Pause_Length: " + str(audio_file.average_pause_length) + "\n\n"
                    )
    data_file.close()

def write_symbol_list(audio_file):
    """
    """
    #print(suffix)
    symbol_file = open("./output" + audio_file.folder_dir + "symbols.txt", "w+")
    symbol_file.write(str(audio_file.symbols))
    symbol_file.close()

    parameters_file = open("./output" + audio_file.folder_dir + "input_entropy_parameters.txt", "w+")
    parameters_file.write("Symbols \n Number of Symbols: " + str(len(audio_file.symbol_model)+1) + "\n "
                            "Symbol Model: " + str(audio_file.symbol_model) + " else " + chr(65+len(audio_file.symbol_model)) + "\n "
                            "Symbols produced: " + str(len(audio_file.symbols)) + "\n\n" )

def read_symbol_list(audio_file):
    """

    """
    symbol_file = open("./output" + audio_file.folder_dir + "symbols.txt", "r")
    symbol_read = symbol_file.read()
    symbol_read = symbol_read.strip('[').strip(']').replace(',', '').replace('\'','').split(' ')
    audio_file.symbols = []
    for symbol in symbol_read:
        audio_file.symbols.append(symbol)
    symbol_file.close()

    data_file = open("./output" + audio_file.folder_dir + "output_data.txt", "a+")
    data_file.write("Symbols \n "
                    "Symbol Occurrence: " + str(audio_file.symbol_occurrence) + "\n "
                    "Ranked Probability: " + str(audio_file.ranked_probability) + "\n\n "
                    )
    data_file.close()

def write_entropy_profile(audio_file):
    """
    """
    create_folder(audio_file.entropy_directory)
    symbol_file = open(audio_file.entropy_directory + "entropy_profile.txt", "w+")
    symbol_file.write(str(audio_file.entropy_profile))
    symbol_file.close()
    
    parameters_file = open("./output" + audio_file.folder_dir + "input_entropy_parameters.txt", "a+")
    parameters_file.write("Entropy \n "
                        "M: " + str(audio_file.M) + "\n "
                        "ap: " + str(audio_file.ap) + "\n "
                        "bp: " + str(audio_file.bp) + "\n "
                        "cp: " + str(audio_file.cp) + "\n "
                        "window_size: " + str(audio_file.window_size) + "\n "
                        "window_overlap: " + str(audio_file.window_overlap) + "\n\n"
    )   
    parameters_file.close()

def write_plot_parameters(audio_file):
    #file_path, file_name, pauses, title, bins, bin_range, show_plot=False)
    """
    """
    parameters_file = open("./output" + audio_file.folder_dir + "input_plot_parameters.txt", "w+")
    parameters_file.write("Plots \n Histogram \n  "
                        "Bins: " + str(audio_file.bins) + "\n  "
                        "Bin Range: " + str(audio_file.bin_range).strip('(').strip(')') + "\n  "
    )   
    parameters_file.close()

def write_pause_averages(directory, binary_pause_array_length, total_audio_pause, total_sounding, pause_proportion, number_of_pauses, pause_length):
    pause_file = open("./output" + directory + "averages.txt", "w+")
    pause_file.write(
                        "File: all \n "
                        "Audio Length: -- \n "
                        "Binary Pause Array Length: " + str(binary_pause_array_length) + "\n "
                        "Total Audio Pause: " + str(total_audio_pause) + "\n "
                        "Total Sounding: " + str(total_sounding) + "\n "
                        "Pause Proportion: " + str(pause_proportion) + "\n "
                        "Number of Pauses: " + str(number_of_pauses) + "\n "
                        "Pause Length: " + str(pause_length) + "\n "
                    )
    pause_file.close()




