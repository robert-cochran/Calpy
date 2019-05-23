from .. import dsp
from .. import plots
from ..utilities import read_wavfile
from ..entropy import symbolise_speech, entropy_profile
import numpy as np
import json
import calpy.pause.file_handling as file_handling
import calpy.pause.data_handling as data_handling
import calpy.entropy as entropy
import calpy.plots as plots
from calpy.pause import parameters 
import time
import datetime
import numpy
#import file_handling as fh

#---OBJECTS---
class AudioFile:
    def __init__(self, audio_folder_dir, audio_file_number, audio_file_frequency, min_silence, compute, printing):
        ''' Contains all the data needed to: 
                compute pause digitisation, 
                write and read, 
                produce plots
            ----------------------
            Variables:
                File Handling
                    audio_file_path, 
                    file_name, e.g. 
                    file_number, 
                    file_frequency,
                    min_silence

                Digitisation
                    binary_pauses e.g. [0,1,1,0,0,1,1,1,...]
                    pauses e.g. [12,4,90,2,2,2,70,...]
                    time_stamp i.e. creation date for files e.g. 04-08-2019
                    binary_length i.e. the length of binary_pauses (~audio_file_length)
                    audio file length (see binary_length)
                    total_pauses i.e. sum of all the 0's (is zero pause?) or frequencies
                    total_sounding
                    number_of_pauses i.e. how many groups of pauses were there (silence bookended by sound)
                    number of sounds - not done
                    pause_proportion
                    average_pause_length
                
                Symbolisation
                    symbol_model
                    symbol_occurrence
                    ranked_probability

                Entropy
                    self.compute_entropy
                    self.selected_symbol = selected_symbol
                    self.M = M
                    self.ap = ap
                    self.bp = bp
                    self.cp = cp 
                    self.window_size = window_size
                    self.window_overlap = window_overlap
                    self.entropy_directory 
                    self.entropy_profile
                    
                Plots
                    self.bins = bins
                    self.bin_range = bin_range
                    self.title = 'Total Pauses vs Sounding counts in conversation ' + self.file_number
                    self.xlabel = 'Group'
                    self.ylabel = 'Individual millisecond counts'
                    self.figure_file_name = 'binary_pause_bar_chart.png'
                    self.x_objects = ('Pauses', 'Sounding')
                    self.y_pos = np.arange(len(self.x_objects))
                    self.y_performance = [self.total_pauses, self.total_sounding]
                    self.opacity = 0.5
                
            ----------------------
            Functions:
                Compute pauses from audio
        '''
        self.file_number = audio_file_number
        self.file_frequency = audio_file_frequency
        self.folder_dir = audio_folder_dir + audio_file_number + '/' + audio_file_frequency + '/'
        self.file_name = self.file_number + '_' + self.file_frequency
        self.audio_file_path = self.folder_dir + self.file_name + '.wav'
        self.min_silence = min_silence
        self.printing = printing
        #self.symbol_model = None
        """
            Possibly move all parameters into init and set to none initially
        """
        if self.printing:
            print(self.audio_file_path)
    
    #---DIGITISATION---
    def pause_digitisation(self, compute):
        def compute_binary_pauses_from_audio(self):
            '''
                Computes the binary pause and pause frequency for the attached audio file
            '''
            
            #--------pause array generation--------
            if self.printing:
                print("digitizing pauses in audio file %s, \n grab a coffee (5-10 minutes wait time)" % (self.audio_file_path))
            
            self.binary_pauses = data_handling.get_pause_digitized('./data' + self.audio_file_path) 
                #e.g. audio file becomes -> [0,0,1,1,0,1,0,0,1,1,0,1...]
            
            if self.printing:
                print("digitizing done")

        def write_binary_pauses_to_file(self):
            """
                This writes binary_pauses, pauses, parameters and data to file
            """
            #-----------
            #folder creation
            #-----------
            if self.printing:
                print("creating dir and writing pauses to file")
            file_handling.create_folder('./output' + self.folder_dir)
            file_handling.write_binary_pause(self) 
        
        def read_binary_pauses_from_file(self):
            """
                Desc:
                    Reads binary pauses and pauses from file
            
            """
            if self.printing:
                print("reading pauses from file")
            file_handling.read_binary_pause(self)

            self.pauses = data_handling.get_pause_frequencies(self.binary_pauses) 
                # e.g. binary pause becomes -> [32,64,2,3,3,2,109...]

            self.time_stamp = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            self.binary_length = len(self.binary_pauses)
            self.number_of_pauses = len(self.pauses)
            self.total_pauses = self.binary_length - sum(self.binary_pauses)
            self.total_sounding = self.binary_length - self.total_pauses
            self.pause_proportion = self.total_pauses/self.binary_length
            self.average_pause_length = self.total_pauses/self.number_of_pauses 
        
        def write_pause_info_to_file(self):
            if self.printing:
                print("writing pause info to file")
            file_handling.write_pause_info(self)

        if compute:
            compute_binary_pauses_from_audio(self)
            write_binary_pauses_to_file(self)
        read_binary_pauses_from_file(self)
        write_pause_info_to_file(self)
       

    #---SYMBOLISATION---
    def symbolize(self, symbol_model):
        self.symbol_model = symbol_model
        self.symbol_occurrence = []
        self.ranked_probability = []
        # print(self.symbol_model)
        self.symbols_in_model = [chr(i+65) for i in range(len(self.symbol_model)+1)]
        self.symbols = []
        # print(self.symbols[0])
        # print([self.symbols[i] for i in range(len(self.symbols))])

        def compute_symbols(self):
            """Computes entropy symbols
            
                To Do:
                    Compute symbols based on symbol_model
            """
            if self.printing:
                print("computing entropy symbols")

            
            symbol = ''
            found = False
            for pause in self.pauses:
                for symbol in range(len(self.symbol_model)):
                    if (pause < self.symbol_model[symbol]) and (not found): #or ((i+1) == len(self.symbol_model)):
                        found = True
                        self.symbols.append(chr(65+symbol)) #chr(65) = 'A'
                if not found:
                    self.symbols.append(chr(65+len(self.symbol_model)))
                    #print(chr(65+2))
                found = False
            # print(len(self.symbols))
            # print(len(self.pauses))
        
        def compute_symbol_occurrences(self):
            self.symbol_occurrence = []
            self.ranked_probability = []
            
            #finding the counts of each letter in the symbol set
            symbols_string = str(self.symbols)
            for i in range(len(self.symbol_model)+1):
                self.symbol_occurrence.append(symbols_string.count(chr(65+i)))
            
            #ranking the probabilities
            symbol_occurrence = self.symbol_occurrence.copy()
            for i in range(len(symbol_occurrence)):
                result = numpy.where(symbol_occurrence == numpy.amax(symbol_occurrence))
                #if 2 or more symbols have equal occurrence, pick the first
                if len(result[0]) > 1:
                    max_index = int(result[0][0])
                else:
                    max_index = int(result[0])
                occurrence = symbol_occurrence[max_index]
                letter = chr(65+max_index)
                self.ranked_probability.append((occurrence, letter)) 
                symbol_occurrence[max_index] = -1
        
            # print(sum(self.symbol_occurrence))
            # print(symbol_occurrence)

        def write_symbols_to_file(self):
            """Writes entropy to file given pause freq data

                Desc:
                    Creates list to bin all symbols appropraitely then sends off to X to write to file 

                Desc:
                    Ex. [AAAABCBAAABAAABABDBDBBAAAAAAACCDGHAAAAAIAAAAH]
            """
            if self.printing:
                print("writing entropy symbols to file")
            file_handling.write_symbol_list(self)
        
        def read_symbols_from_file(self):
            """Reads symbols from file into an array
            
                Desc:
                    Essentially just the same as read_pauses_from_file, I just wanted 
                        everything to be organized into the order of operations

                Args:
                    file_path: ....

                Returns:
                    symbols: list
                        the list of symbols retrieved from file
            """
            if self.printing:
                print("reading entropy symbols from file")
            file_handling.read_symbol_list(self)

            # if fast_entropy:
            #     "to do"
            # else:
            #     return(ce.entropy_profile(symbols,window_size=1))

        compute_symbols(self)
        compute_symbol_occurrences(self)
        write_symbols_to_file(self)
        read_symbols_from_file(self)

    #---ENTROPY---
    def entropy(self, selected_symbol, M, ap, bp, cp, window_size, window_overlap):
        self.compute_entropy #??
        self.selected_symbol = selected_symbol
        self.M = M
        self.ap = ap
        self.bp = bp
        self.cp = cp 
        self.window_size = window_size
        self.window_overlap = window_overlap
        self.entropy_directory = "./output" + self.folder_dir + "entropy/window_size=" + str(self.window_size) + '/window_overlap=' + str(self.window_overlap) + "/"
        self.entropy_profile = []

        self.compute_entropy()
        self.write_entropy_profile_to_file()      
    def compute_entropy(self):
        if self.printing:
            print("computing entropy profile based on symbol set provided")
        #self.entropy_profile = entropy.fast_entropy_profile(self.symbols, self.selected_symbol,self.M,self.ap,self.bp,self.cp,self.window_size,self.window_overlap)
        self.entropy_profile = entropy.entropy_profile(self.symbols, self.window_size, self.window_overlap)
    def write_entropy_profile_to_file(self):
        """Writes entropy to file given pause freq data

            Desc:
                Creates list to bin all symbols appropraitely then sends off to X to write to file 
                Ex. [AAAABCBAAABAAABABDBDBBAAAAAAACCDGHAAAAAIAAAAH]
        """
        if self.printing:
            print("writing entropy profile to file")
        file_handling.write_entropy_profile(self)

    #---PLOTS---
    def plots(self, bins, bin_range):
        self.bins = bins
        self.bin_range = bin_range
        self.produce_binary_pause_bar_chart()
        self.produce_pause_histogram()
        self.produce_ranked_probability()
        self.produce_entropy_plots()
        self.write_plot_parameters()
    def produce_binary_pause_bar_chart(self):
        self.title = 'Total Pauses vs Sounding counts in conversation ' + self.file_number
        self.xlabel = 'Group'
        self.ylabel = 'Individual millisecond counts'
        self.figure_file_name = 'binary_pause_bar_chart.png'
        self.x_objects = ('Pauses', 'Sounding')
        self.y_pos = np.arange(len(self.x_objects))
        self.y_performance = [self.total_pauses, self.total_sounding]
        self.opacity = 0.5
        if self.printing:
            print('Producing pause plots of binary pauses') 
        plots.bar(self)
    def produce_pause_histogram(self):
        """All Data Plots 

            Desc:
                All plots for raw pause histograms, freq histograms, entropy plots, etc...


            To Do:
                Normalize plot axis
                Label axis
                Proper Descriptive Title

        """
        if self.printing:
            print("producing pause histogram")
        plots.histogram(self)
    def produce_ranked_probability(self):
        """Outline
        
            Sum up the occurrence of A's, B's, etc..
            Plot each one as a bar in a bar chart

            then I can use this to see if others follow the same distribution

            then ill need another function that plots two models against each other, 
                so maybe a bar chart overlayed with a horizontal linegraph showing how one stacks up to the other, 
                or maybe stacked bar graph?
        """
        if self.printing:
            print("producing ranked probability plot")

        self.title = 'Ranked Probability of symbols for conversation ' + self.file_number
        self.xlabel = 'Symbols'
        self.ylabel = 'Symbol counts'
        self.figure_file_name = 'ranked probability.png'
        self.x_objects = []
        self.y_performance = []
        for i in range(len(self.ranked_probability)):
            occurrence = self.ranked_probability[i][0]
            letter = self.ranked_probability[i][1]
            self.x_objects.append(letter)
            self.y_performance.append(occurrence)
        self.y_pos = np.arange(len(self.x_objects))
        self.opacity = 0.5
        plots.bar(self)
    def produce_entropy_plots(self):
        #file_path = "./output" + audio_file.folder_dir + "/pause_histogram.png"
        title = "Entropy Profile - Window Size (" + str(self.window_size) + ") Overlap (" + str(self.window_overlap) + ")"
        file_path = self.entropy_directory
        if self.printing:
            print("writing anomaly plot to file")
        plots.profile_plot(self.entropy_directory, title, self.entropy_profile, figsize=(25,4)) #needs title, finer grained x, axis labels
    def write_plot_parameters(self):
        if self.printing:
            print("writing plot parameters to file")
        file_handling.write_plot_parameters(self)



