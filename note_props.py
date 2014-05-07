 #!/usr/bin/python
 
from music21 import *
import string

alph = dict.fromkeys(string.ascii_uppercase[0:7], 0)


class Chord:
  ''' A simple chord class'''
  def __init__(self, vector):
    self.v = vector
    
    
  
def main():
  hymn = converter.parse('Think_of_Me_-_Flute_Trio.mxl')
  
  for part in hymn.parts:
    for note in part.flat.elements:
      if dict[note.name]:

      

if __name__ == '__main__':
  main()