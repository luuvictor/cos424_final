 #!/usr/bin/python -tt


from music21 import *
import string
from to_array import transpose

# part_id is a string, e.g . 'Alto'
def replaceAlto(old_score, list_notes, part_id, clef_name):
  
  s = old_score
  old_part = None
  
  for part in s.parts:
    #print part.id
    #if (str(s.id) == str(part_id)):
    if ('Alto' in str(part.id)):
     old_part = part
  if old_part == None:
    print part_id
    print 'part_id doesn\'t seem to match any part in the old_score!!!!'
    return None
  
  # GET JUNK FROM THE OLD STREAM 
  newPart = stream.Part()
  
  ins = instrument.fromString(part_id)
  cl = clef.clefFromString(clef_name)
  ks = old_part.flat.getElementsByClass(key.KeySignature)[0]
  ts = meter.TimeSignature('c')
  sy_layout = old_part.flat.getElementsByClass(layout.SystemLayout)[0]
  #st_layout = old_part.flat.getElementsByClass(layout.StaffLayout)[0]
  
  
  newPart.insert(0, ins)
  
  #ADD JUNK TO THE NEW STREAM
  
  m1 = stream.Measure()
  m1.insert(0, cl)
  m1.insert(0, ks)
  m1.insert(0, ts)
  m1.insert(0, sy_layout)
  #m1.insert(0, st_layout)
  
  # ADD NOTES TO THE FIRST MEASURE
  for i in range(4):
    n = list_notes[i]
    if n == 1000: item = note.Rest()
    else:
      p = pitch.Pitch()
      p.midi = n
      item = note.Note(p.name)
    m1.insert(i, item)
  
  
  #ADD NOTES TO THE OTHER MEASURES
  
  i = 0 # a fun little counter thing
  j = 0
  curr_measure = m1
  for n in list_notes[4:]:
    i = i % 4
    if i == 0:
     newPart.insert(j*4, curr_measure)
     curr_measure = stream.Measure()
     j = j+1   
    if n == 1000: item = note.Rest()
    else:
      p = pitch.Pitch()
      p.midi = n
      item = note.Note(p.name)
    curr_measure.insert(i, item)
    i = i+1 
  
  newPart.show('text')
  s.insert(4,newPart)
  print s
  return s


def midiToNote(midi_number):
  m = midi_number
  
  if m == 1000: item = note.Rest()
  else:
    p = pitch.Pitch()
    p.midi = m
    item = note.Note(p.name)
  return item
  
  

def replaceAltoBETTER(old_score, list_notes, part_id, clef_name):
  s = old_score
  old_part = None
  
  for part in s.parts:
    #print part.id
    #if (str(s.id) == str(part_id)):
    if ('Alto' in str(part.id)):
     old_part = part
  if old_part == None:
    print part_id
    print 'part_id doesn\'t seem to match any part in the old_score!!!!'
    return None
  
  
  newPart = stream.Part()
  
  ins = instrument.fromString(part_id)
  cl = clef.clefFromString(clef_name)
  ks = old_part.flat.getElementsByClass(key.KeySignature)[0]
  ts = meter.TimeSignature('c')
  sy_layout = old_part.flat.getElementsByClass(layout.SystemLayout)[0]
  #st_layout = old_part.flat.getElementsByClass(layout.StaffLayout)[0]
  
  
  newPart.insert(0, ins)
  
  m1 = stream.Measure()
  m1.insert(0, cl)
  m1.insert(0, ks)
  m1.insert(0, ts)
  m1.insert(0, sy_layout)
  #m1.insert(0, st_layout)
  
  notes = [midiToNote(x) for x in list_notes] #notes is a list of actual list objects
  for n in notes:
    newPart.append(n)
  
  newPart.show('text')
  s.insert(4,newPart)
  print s
  return s
  

def main():
  
  
  
  filename =  'MAJORbwv436.mxl.csv'
  stitchFilename=filename[5:]
  #data=[['Cmajor', 59], ['Cmajor', 60], ['Aminor', 60], ['Dmajor', 62], ['Gmajor', 62], ['Cmajor', 67], ['Fmajor', 60], ['Cmajor', 55], ['Fmajor', 60], ['Gmajor', 59], ['Cmajor', 59], ['Cmajor', 60], ['Cmajor', 60], ['Fmajor', 60], ['Cmajor', 59], ['Cmajor', 60], ['Cmajor', 60], ['Fmajor', 60], ['Cmajor', 59], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Dminor', 60], ['Gmajor', 62], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 55], ['Fmajor', 60], ['Gmajor', 59], ['Cmajor', 59], ['Cmajor', 60], ['Aminor', 60], ['Dmajor', 62], ['Gmajor', 62], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 67], ['Cmajor', 67], ['Cmajor', 67], ['Fmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 55], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 55], ['Fmajor', 60], ['Gmajor', 59], ['Cmajor', 59], ['Cmajor', 60], ['Aminor', 60], ['Dmajor', 62], ['Gmajor', 62], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 67], ['Cmajor', 67], ['Cmajor', 67], ['Fmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 55], ['Cmajor', 60], ['Fmajor', 60], ['Fmajor', 60], ['Fmajor', 1000], ['Fmajor', 60], ['Fmajor', 60], ['Cmajor', 59]]
  data=[['Aminor', 60], ['Dmajor', 62], ['Gmajor', 62], ['Cmajor', 67], ['Fmajor', 60], ['Cmajor', 55], ['Fmajor', 60], ['Gmajor', 59], ['Cmajor', 59], ['Cmajor', 60], ['Cmajor', 60], ['Fmajor', 60], ['Cmajor', 59], ['Cmajor', 60], ['Cmajor', 60], ['Fmajor', 60], ['Cmajor', 59], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Dminor', 60], ['Gmajor', 62], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 55], ['Fmajor', 60], ['Gmajor', 59], ['Cmajor', 59], ['Cmajor', 60], ['Aminor', 60], ['Dmajor', 62], ['Gmajor', 62], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 67], ['Cmajor', 67], ['Cmajor', 67], ['Fmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 55], ['Cmajor', 60], ['Cmajor', 60], ['Cmajor', 55], ['Fmajor', 60], ['Gmajor', 59], ['Cmajor', 59], ['Cmajor', 60], ['Aminor', 60], ['Dmajor', 62], ['Gmajor', 62], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 67], ['Cmajor', 67], ['Cmajor', 67], ['Fmajor', 60], ['Cmajor', 60], ['Cmajor', 60], ['Gmajor', 62], ['Gmajor', 62], ['Gmajor', 62], ['Cmajor', 55], ['Cmajor', 60], ['Fmajor', 60], ['Fmajor', 60], ['Fmajor', 1000], ['Fmajor', 60], ['Fmajor', 60], ['Cmajor', 59]]
  filename = "bwv436"
  list_notes = [x[1] for x in data]
  
  
  # stitchFilename='bwv436.mxl.csv'
  # #list_notes =  [1000, 1000, 1000, 55, 62, 60, 57, 59, 64, 62, 62, 60, 60, 65, 67, 62, 67, 62, 62, 60, 60, 62, 60, 60, 60, 59, 55, 55, 62, 60, 57, 59, 64, 62, 62, 60, 60, 65, 67, 62, 67, 62, 62, 60, 60, 62, 60, 60, 60, 59, 55, 55, 62, 62, 60, 60, 62, 62, 60, 60, 62, 60, 59, 60, 62, 60, 59, 60, 62, 60, 57, 59, 55, 55, 64, 66, 64, 59, 60, 60, 57, 59]
  # list_notes =  [62, 60, 57, 59, 64, 62, 62, 60, 60, 65, 67, 62, 67, 62, 62, 60, 60, 62, 60, 60, 60, 59, 55, 55, 62, 60, 57, 59, 64, 62, 62, 60, 60, 65, 67, 62, 67, 62, 62, 60, 60, 62, 60, 60, 60, 59, 55, 55, 62, 62, 60, 60, 62, 62, 60, 60, 62, 60, 59, 60, 62, 60, 59, 60, 62, 60, 57, 59, 55, 55, 64, 66, 64, 59, 60, 60, 57, 59]
  # 
  #filename = 'bwv436'
  
  #list_notes = [62, 55, 57, 59, 64, 62, 62, 64, 65, 65, 67, 62, 62, 62, 59, 60, 60, 59, 60, 60, 60, 59, 55, 55, 62, 55, 57, 59, 64, 62, 62, 64, 65, 65, 67, 62, 62, 62, 59, 60, 60, 59, 60, 60, 60, 59, 55, 55, 62, 62, 60, 60, 62, 62, 60, 60, 62, 60, 59, 60, 62, 60, 59, 60, 62, 60, 57, 59, 55, 55, 64, 63, 64, 64, 60, 60, 60, 59]

  #list_notes = [60, 60, 60, 60, 60, 60, 60, 59, 59, 59, 57, 57, 55, 55, 52, 54, 55, 62, 55, 59, 57, 55, 55, 55, 55, 55, 55, 55, 55, 55, 57, 60, 60, 60, 60, 60, 60, 60, 60, 59, 59, 59, 57, 57, 55, 55, 52, 54, 55, 62, 55, 59, 57, 55, 55, 55, 55, 55, 55, 55, 55, 60, 60, 60, 60, 59, 59, 59, 57, 57, 57, 56, 56, 59, 52, 56, 57, 52, 52, 52, 52, 52, 52, 52, 55, 55, 55, 55, 55, 60, 62, 60, 60, 59, 59, 59, 60, 55, 55, 59, 55, 55, 59, 62, 60, 60, 57, 55, 55, 55]
  #filename = 'bwv433'

  score = corpus.parse(filename)
  score_C = transpose(score)
  score.show()
  #list_notes = [60, 62, 64, 65, 67, 69, 60, 60, 60, 60, 60]
  
  replaceAltoBETTER(score_C, list_notes, "Alto", "G4").show()




if __name__ == '__main__':
  main()