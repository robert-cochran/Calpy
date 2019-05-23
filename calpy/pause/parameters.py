'''PARAMETERS'''
#----------Settings----------

#-----DIGITISATION-----
compute = False
printing = False #Recommended to leave true when computing since it takes so long
min_silence = 0.001 #milli is .001

#-----SYMBOLISATION-----
#symbol_model = [20,40,60,80,100,200,400,800]
#symbol_model = [2, 5, 10, 20, 50, 100, 200]
# symbol_model = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20]
symbol_model = [3, 6, 10, 15]
symbols_suffix = "/symbol_list"

#-----ENTROPY-----
M = 27
ap = 0.0073
bp = 4.2432
cp = 4.2013
window_size = 150 #100 previously, why 100??? Need to justify!
window_overlap = 149 #10 previously, why 5??? Need to justify!
selected_symbol = 'A' #'''why A, why not C or B or D?''' Need to Justify!

#-----PLOTS-----
#---single pause--- i.e. [0,1,0,0,1,0]
pause_bins = 2
pause_bin_range = (0,1)
#---pause lengths--- i.e. [123,4,23,23,24,1,90]
bins = 20
bin_range = (0,100)
#---entropy---