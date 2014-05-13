 #!/usr/bin/python -tt


import sys, os, ast, csv
from music21 import *

# the column numbers of key data in victor's CSV format
S_IND = 0
A_IND = 1
T_IND = 2
B_IND = 3


#columns that contain alto predictions
PRED_COL_NAMES = ['simple2','simple3','simple1','simple7','simple6','viterbi4','viterbi8']
HEADER_ADDITIONS  = [x + 'CHORD' for x in PRED_COL_NAMES]


def main():
  dir_in = sys.argv[1] # input is a directory name
  dir_out = sys.argv[2] #will make this direcrtory if necessary 
  
  if not os.path.exists(dir_out): os.mkdir(dir_out)
  
  filenames = os.listdir(dir_in)
  for fn in filenames:
    if fn[-4:] != '.csv': continue
    print fn
    f_in  = open(os.path.join(dir_in,fn),'rU')
    f_out = open(os.path.join(dir_out,'CHORDS_' + fn),'w')
    add_chord_names(f_in,f_out)


def add_chord_names(csvfile_in, csvfile_out):
  reader = csv.reader(csvfile_in) # a reader object
  writer = csv.writer(csvfile_out)
  
  header = reader.next()
  pred_inds = [header.index(n) for n in PRED_COL_NAMES]
  new_header = header + HEADER_ADDITIONS #add in the new column names for the chords
  
  writer.writerow(new_header)
  
  for row in reader:
    if row == []: continue
    if row[0] == '': continue # every other line seems to be blank in these files. One of these calls will skip the row
    #print row
    ##get soprano, tenor, and base chords
    #print row[S_IND]
    S = abs(int(row[S_IND]))
    T = abs(int(row[T_IND]))
    B = abs(int(row[B_IND]))
    
    row_addition = ['NOT_FOUND']*len(PRED_COL_NAMES) 
    for i in range(len(PRED_COL_NAMES)):
      try:
        n = pred_inds[i]
        newA = abs(int(row[n]))
        chord_array = [S, newA, T, B] 
        c = chord.Chord([S,abs(int(row[n])),T,B])
        chord_array = [x for x in chord_array if x != 1000]
        row_addition[i] = c.root().name + c.quality
      except:
         print 'There is a problem in:', csvfile_in,'row looks like:', row
             
    writer.writerow(row + row_addition)

  







if __name__ == "__main__":
    main()