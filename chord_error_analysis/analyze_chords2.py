 #!/usr/bin/python -tt


import sys, os, ast, csv
from addAlto import actuallyReplaceAlto
from to_array import transpose
from music21 import *

# the column numbers of key data in victor's CSV format
S_IND = 0
A_IND = 1
T_IND = 2
B_IND = 3


#columns that contain alto predictions
PRED_COL_NAMES = ['simple2','simple3','simple1','simple7','simple6','viterbi4','viterbi8']
HEADER_ADDITIONS  = [x+'CHORD' for x in PRED_COL_NAMES]


def main():
  dir = sys.argv[1] # input is a directory name
  filenames = os.listdir(dir)
  for fn in filenames:
    if f[-4] != '.csv': continue
    f = open(fn,'rU')
    add_chord_names(f)


def add_chord_names(csvfile):
  reader = csv.reader(csvfile) # a reader object
  header = reader.next()
  pred_inds = [header.index(n) for n in PRED_COL_NAMES]
  new_header = header + HEADER_ADDITIONS #add in the new column names for the chords
  for row in reader:
    if row == []: continue # every other line seems to be empty in these files...
    
    # get soprano, tenor, and base chords
    S = int(row[S_IND])
    T = int(row[T_IND])
    B = int(row[B_IND])
    for n in pred_inds:
      c = chord.Chord(S,int(row[n]),T,B)
      print c.root().name + c.quality
      

    







if __name__ == "__main__":
    main()