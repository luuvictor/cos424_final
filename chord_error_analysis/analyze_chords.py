 #!/usr/bin/python -tt


import sys, os, ast
from addAlto import actuallyReplaceAlto
from to_array import transpose
from music21 import *

def main():
  '''this code calls chordify on the original and reconstructed tracks, and compares the results'''
  if len(sys.argv) < 3:
    print 'Usage: python analyze_chord.py [-d OR -s] [dir_name OR fn.csv]'
    sys.exit(1)
  if sys.argv[1] == '-s':
    fn = sys.argv[2] # eg 'bwv411'
    pn = fn.split('/')[-1][:-8] #I am so sorry for this monster. It is just supposed to exttract the corpus name :/
    s = corpus.parse(pn)
    s = transpose(s)
    
    list_notes = ast.literal_eval(open(fn,'rU').read())

    actuallyReplaceAlto(s, list_notes,'Alto','G4')
    s.show()
    chord_names = return_chord_names(s)
    
    note_and_chord = [[list_notes[i],chord_names[i]] for i in range(len(list_notes))]
    print note_and_chord
      
      


def return_chord_names(s):
  '''given a stream and the key its in, returns the root+mode (e.g. 'Cmajor')'''
  sChords = s.chordify()
  print 'hello my name is return_chord_names. You killed my parent directory. Prepare to die.'
  sChords.id = 'AddedChords'
  chords = sChords.flat.getElementsByClass(chord.Chord)
  
  out = []  
  i = 0.0
  curr_chord_name = 'Cmajor'  #just default to c major at the beginning
  while(True):
    if i > chords.highestOffset: break
    c = chords.getElementsByOffset(i)
    if len(c): curr_chord_name = (c[0].root().name + c[0].quality) #update current chord if possible. Otherwise hold out
    out.append(curr_chord_name)
    i = i + 1.0
  return out
  
  







if __name__ == "__main__":
    main()