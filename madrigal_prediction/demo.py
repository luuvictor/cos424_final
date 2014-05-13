 #!/usr/bin/python -tt

from addAlto import replaceAltoBETTER
from to_array import transpose
from music21 import *
import sys, os, ast

dirs = ['simple2','simple3','simple1','simple7','simple6','viterbi4','viterbi8']
#dirs = ['simple2','simple1', 'simple6','viterbi4']

#the call we need is: replaceAltoBETTER(old_score, list_notes, part_id, clef_name)




def main():
  work_name = sys.argv[1] #e.g. 'bwv411'
  file_name = work_name + '.mxl.csv'
  
  score = corpus.parse(work_name)
  score_C = transpose(score)
  score.show() # original score
  
  
  for d in dirs:
    # need to reset the score... can definitely do this more efficiently!
    score = corpus.parse(work_name)
    score_C = transpose(score)
    
    path = os.path.join(d, file_name)
    list_notes = ast.literal_eval(open(path,'rU').read())
    if 'viterbi' in d:
      list_notes =  [x[1] for x in list_notes]

    
    print list_notes
    replaceAltoBETTER(score, list_notes, 'Alto', 'G4')
    score.show()
  

  
  









if __name__ == "__main__":
    main()