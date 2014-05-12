from music21 import *
import csv
import sys
from os import listdir
import os

def toPair(t):
    return ('\"' + str(t[0]) + '\":\"' + str(t[1]) + '\"')

def addToDict(target_dict, time, key, value):
    if not time in target_dict:
        target_dict[time] = []
        
    # target_dict[time].append(toPair((key, value)))
    target_dict[time].append(value)
    return target_dict    

def getArray(mxl):
    work = corpus.parse(mxl)
    #work = converter.parse("C:\\Python27\\lib\\site-packages\\music21\\corpus\\bach\\bwv227.11.mxl")
    work = transpose(work)
    work = add_chords(work)
    # work.show()
    return work

def add_chords(s):
  '''given a stream and the key its in, adds a new part called 'chords' which has the closed form of the chords
  make by the other parts at the latin name of the chords as lyrics to that track'''
  sChords = s.chordify()
  sChords.id = 'AddedChords'
  s.insert(0, sChords)
  for c in sChords.flat.getElementsByClass('Chord'):
    c.closedPosition(forceOctave=4, inPlace=True)
  return s

def transpose(s):
  '''given a (multipart) stream, return a stream that is transposed to C major (if major)
   or a minor (if minor). Handles key changes by converting each new key signature back to 
   C or a minor. Probably changes the original stream. Sorry. Or not.'''
  currPitch = pitch.Pitch('C')
  currMode = 'major'
  target = (pitch.Pitch('C'))
  inter = interval.Interval(currPitch, target)
  for part in s.parts:
    print part 
    measures = part.getElementsByClass(stream.Measure)
    for m in measures:
      k = m.getElementsByClass(key.KeySignature)
      if len(k):
        p, mode = k[0].pitchAndMode
        if p and mode:
          print p, mode
          if mode == u'major': target = pitch.Pitch('c') 
          if mode == u'minor':
             target = pitch.Pitch('a')
             # print 'hello'
          inter = interval.Interval(p,target)
        k[0].transpose(inter, inPlace=True)
        print k[0]
      m.transpose(inter, inPlace=True)
  return s

def get_offset(music21_score):
    offset = 0
    valid = 1
    work = music21_score
    try:
        measure_offsets = work.measureOffsetMap().keys()
        measure_offsets.remove(0.0)
        offset = min(measure_offsets)
        TS = work.getTimeSignatures()[0]
        print TS.ratioString
        ratioStr = "TS" + TS.ratioString.replace('/', '-')        
        if ratioStr == "TS4-4":       # TODO         
            offset = 4 - offset
        else:
            print "new time signature"
            valid = 0            
    except Exception:
        print "offsetmap broken"
        valid = 0
    return (valid, offset)

def corpus_to_array(music21_score):
    # piece = corpus.parse(filename)
    piece = music21_score
    parts = piece.parts
    num_parts = len(parts)

    # store most recent thing being played 
    lastPitch = [1000]
    currentOffset = 0;

    # a "measures:" list contains "beats" objects
    # "beats" contains 8 "beat" objects
    # "beat" object - "time", "chord", "s", "a", "t", "b"

    # 1. make a big dictionary (time -> info)
    #       only the "first" part of each entry needs to "initialize row"

    # 2. go through the big dictionary in TIME order
    #       - group each set of 8 elements into a list L "beats"
    #           - make sure that list L is "indexed" correctly
    #       - add all of the list Ls one big list of lists "measures"

    # step one, declare 2d matrix

    valid, offset = get_offset(piece)
    print "offset: ", offset
    if valid == 0:
        print "time/offset error with this note"
        return None
    
    full_times = {}

    SONG_KEY = piece.analyze('key')
    print "songkey", SONG_KEY 
    
    for part_num in range(num_parts):
        # print in order, each note
        lastPitch = [1000]
        currentOffset = 0;

        print piece.parts[part_num].id      
        for n in piece.parts[part_num].flat.notes:          

            if piece.parts[part_num].id != "Soprano" and piece.parts[part_num].id != "Alto" and piece.parts[part_num].id != "Tenor" and piece.parts[part_num].id != "Bass" and piece.parts[part_num].id != "AddedChords":
            # if piece.parts[part_num].id != "Soprano" and piece.parts[part_num].id != "Alto" and piece.parts[part_num].id != "Tenor" and piece.parts[part_num].id != "Bass":
                continue
                                
            # fill in gap since last note
            this_note_offset = n.offset + offset;

            modulo = (this_note_offset * 4) % 4
            # roundup = 0
            if modulo == 1 or modulo == 3:
                continue #skip the 16th notes!
#                print "16th", this_note_offset
            

            ############
            while currentOffset < this_note_offset:
                for pitch_num in lastPitch:
                    if piece.parts[part_num].id == "AddedChords":
                        full_times = addToDict(full_times, currentOffset, piece.parts[part_num].id, pitch_num)
                    else:            
                        full_times = addToDict(full_times, currentOffset, piece.parts[part_num].id, -pitch_num)
                    
                currentOffset += 0.5
            
            # so we now know that currentOffset == this_noteOffset
            if type(n) is note.Note:
                full_times = addToDict(full_times, n.offset + offset, piece.parts[part_num].id, n.midi)
                lastPitch = [n.midi]
            elif type(n) is chord.Chord:
            # we know this is a chord, examine each note within
                lastPitch = []
                # if this is the AddedChord get the correct chord detection
                if piece.parts[part_num].id == "AddedChords":
                    rn = n.root().name + n.quality
                    addToDict(full_times, n.offset + offset, piece.parts[part_num].id, rn)
                    lastPitch = [rn]
                # if this is a normal "voice", arbitrarily choose one of them
                else:                    
                    for pitch in n.pitches: 
                        full_times = addToDict(full_times, n.offset + offset, piece.parts[part_num].id, pitch.midi)
                        lastPitch.append(pitch.midi)
                        break
            # just in case
            elif type(n) is note.Rest:
                full_times = addToDict(full_times, n.offset + offset, piece.parts[part_num].id, 1000)
                lastPitch = [1000]
            else:
                print("unknown type")
                sys.exit()

            # prepare to start examining new notes
            currentOffset += 0.5

    return full_times

def individual_parse_example():
    work = corpus.parse('bach/bwv110.7.mxl')
    #work = converter.parse("C:\\Python27\\lib\\site-packages\\music21\\corpus\\bach\\bwv227.11.mxl")
    work = transpose(work) # jbocarsly addition, transpose
    work = add_chords(work)

    times = corpus_to_array(work)
    if times == None:
        print "invalid"
        sys.exit()

    SOPRANO = 0
    ALTO = 1
    TENOR = 2
    BASS = 3
    CHORD = 4

    my_offset = 0
    tuple_list = times.get(my_offset)
    while tuple_list and my_offset < 10:

        print my_offset, tuple_list[0], tuple_list[4]

        my_offset += 0.5
        tuple_list = times.get(my_offset)

    write_array_to_csv(times, "mycsvtest")

# given a csv format, reads in/out stuff
def read_csv_to_array(filename):

    times = {}

    # make the extra check - everything should be positive (no half notes!)
    # S_minVal = 100
    # S_maxVal = 0
    # A_minVal = 100
    # A_maxVal = 0
    # T_minVal = 100
    # T_maxVal = 0
    # B_minVal = 100
    # B_maxVal = 0

    # print "opening: ", filename
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        counter = 0
        for row in reader:
            # print row
            # for now, stick into the same associative array thing we had before
            timeIndex = float(row[0])

            # this is not a round number, i.e.
            (row_1, row_2, row_3, row_4) = (float(row[1]), float(row[2]), float(row[3]), float(row[4]))            
            
            if (timeIndex - int(timeIndex)) * (timeIndex - int(timeIndex)) < 0.001:
                times[float(row[0])] = (abs(row_1), abs(row_2), abs(row_3), abs(row_4), \
                                        row[5].strip())
            else:
                times[float(row[0])] = (row_1, row_2, row_3, row_4, row[5].strip())            

            continue
            this_S_Value = abs(float(row[1]))
            this_A_Value = abs(float(row[2]))
            this_T_Value = abs(float(row[3]))
            this_B_Value = abs(float(row[4]))
            
            if (this_S_Value != 1000):
                if (this_S_Value > S_maxVal):
                    S_maxVal = this_S_Value
                elif (this_S_Value < S_minVal):
                    S_minVal = this_S_Value

            if (this_A_Value != 1000):
                if (this_A_Value > A_maxVal):
                    A_maxVal = this_A_Value
                elif (this_A_Value < A_minVal):
                    A_minVal = this_A_Value

            if (this_T_Value != 1000):
                if (this_T_Value > T_maxVal):
                    T_maxVal = this_T_Value
                elif (this_T_Value < T_minVal):
                    T_minVal = this_T_Value

            if (this_B_Value != 1000):
                if (this_B_Value > B_maxVal):
                    B_maxVal = this_B_Value
                elif (this_B_Value < B_minVal):
                    B_minVal = this_B_Value

    # write these min/max values to
    # someiterable = [filename, S_minVal, S_maxVal, A_minVal, A_maxVal, T_minVal, T_maxVal, B_minVal, B_maxVal]
    # print someiterable
    
    # with open('range/range.csv', 'a') as f:
    #    writer = csv.writer(f)
    #    writer.writerow(someiterable)
        
    return times

def read_all_csv_chorales():

    buncha_times = {}
    # for workName in corpus.getBachChorales():
    for f in listdir(os.getcwd()):
        #if f.find("bwv1.6") != -1:
        #    continue
        if f.find("csv") == -1:
            continue
        # get simple filename, in csv format
        buncha_times[f] = read_csv_to_array(f)

    return buncha_times
        

def write_array_to_csv(times_array, target_filename):

    target_filename = target_filename + ".csv"
    print target_filename
    file_out = open(target_filename, 'w')
    
    my_offset = 0
    tuple_list = times_array.get(my_offset)    
    while tuple_list:

        print my_offset, tuple_list[0], tuple_list[4]
        file_out.write(str(my_offset) + ', ' + str(tuple_list[0]) + ', ' + str(tuple_list[1]) + ', ' + str(tuple_list[2]) + ', ' + str(tuple_list[3]) + ', ' + str(tuple_list[4]) + '\n')

        my_offset += 0.5
        tuple_list = times_array.get(my_offset)

    file_out.close()
    
def write_chorales_to_csv():

    chorales = {}    
    # read piece
    for workName in corpus.getBachChorales():
        # score object
        try:
            work = converter.parse(workName)
            print(workName + " exists")
            work = transpose(work) # jbocarsly addition, transpose
            work = add_chords(work)

            # obtain array corresponding to music21 score
            times = corpus_to_array(work)

            # easier filename
            names = workName.split('\\')
            # filename = names[len(names) - 1]
            filename = names[-1]

            # write array to csv!            
            write_array_to_csv(times, filename)
            
            print("transposed!")
        except:
            print(workName+ " hit exception continue")
            continue

    return chorales

def read_all_chorales():
    filename = "all_chorales_sample.csv"    
    with open(filename, 'rb') as f:
        reader = csv.reader(f)
        minVal = 100
        maxVal = 0
        for row in reader:
            thisValue = abs(float(row[4]))
            if (thisValue > maxVal):
                maxVal = thisValue
            elif (thisValue < minVal):
                minVal = thisValue

        print maxVal, minVal           

# filename: "bwv67.7.mxl.csv"
# notes, list of quarter notes starting from index 0
def stitchIn(filename, list_notes):

    # filename = "bach\\" + filename
    score = corpus.parse(filename)

    # hard-coded values, just use alto
    part_id = "Alto"
    clef_name = "G4"
    
    replaceAlto(score, list_notes, part_id, clef_name)
    score.show()

def main():
    # chorales = get_chorales()
    # print chorales
    # print chorales[1]
    # individual_parse_example()
    # write_chorales_to_csv()
    # times = read_csv_to_array("bwv1.6.mxl.csv")
    # print "-----times"
    # print times

    # read_all_chorales()

    # all_chorales = read_all_csv_chorales()
    
    ### sample API testing code

    # all_chorales is a dict (filename -> dict)
    # all_chorales[filename] is a dict (time -> 5-tuple)
    all_chorales = read_all_csv_chorales()
    print (all_chorales.keys())
    print "----------done keys"
    print all_chorales["bwv67.7.mxl.csv"]
    print "----------more fun stuff---"
    print sorted(all_chorales["bwv67.7.mxl.csv"].keys())
    print " ------------------------"
    print all_chorales["bwv67.7.mxl.csv"][21.5]
    print " -------------------------"
    print all_chorales["bwv67.7.mxl.csv"][21.5][0], \
          all_chorales["bwv67.7.mxl.csv"][21.5][1], \
          all_chorales["bwv67.7.mxl.csv"][21.5][2], \
          all_chorales["bwv67.7.mxl.csv"][21.5][3]

if __name__ == "__main__":
    main()
