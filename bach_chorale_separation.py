from music21 import *
import sys

# target dict is [ time (double) -> dict (key -> value) ]
#   hashmap[ doubles -> fixed list of tuples ]
# creates the binding if necessary

def toPair(t):
    return ('\"' + str(t[0]) + '\":\"' + str(t[1]) + '\"')

def addToDict(target_dict, time, key, value):
    if not time in target_dict:
        target_dict[time] = []
        
    # target_dict[time].append(toPair((key, value)))
    target_dict[time].append(value)
    return target_dict    

def write_raw(music21_score, newfilename, offset):
    # piece = corpus.parse(filename)
    piece = music21_score
    parts = piece.parts
    num_parts = len(parts)

    # open standard out    
    # newfilename=filename + '.raw'
    file_out = open(newfilename, 'w')
    # sys.stdout = file_out

    # store most recent thing being played 
    lastPitch = [1000]
    currentOffset = 0;

    # a "measures:" list contains "beats" objects
    # "beats" contains 8 "beat" objects
    # "beat" object - "time", "chord", "s", "a", "t", "b"

    # 1. make a big dictionary (time -> info)
    #       substitute all file_out.write with filling in this table
    #           only the "first" part of each entry needs to "initialize row"

    # 2. go through the big dictionary in TIME order
    #       - group each set of 8 elements into a list L "beats"
    #           - make sure that list L is "indexed" correctly
    #       - add all of the list Ls one big list of lists "measures"

    # step one, declare 2d matrix
    full_times = {}

    # SONG_KEY = piece.flat.getElementsByClass(key.KeySignature)[0]
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

            # newfilename = "ROUND" + newfilename            
            modulo = (this_note_offset * 4) % 4
            # roundup = 0
            if modulo == 1 or modulo == 3:
                print "16th", this_note_offset
                continue #skip the 16th notes!

            ############
            while currentOffset < this_note_offset:
                for pitch_num in lastPitch:
                    if piece.parts[part_num].id == "AddedChords":
                        file_out.write(str(currentOffset) + '\t' + str(pitch_num) + '\t' + piece.parts[part_num].id + '\n')
                        full_times = addToDict(full_times, currentOffset, piece.parts[part_num].id, pitch_num)
                    else:
                        file_out.write(str(currentOffset) + '\t' + str(-pitch_num) + '\t' + piece.parts[part_num].id + '\n')
                        full_times = addToDict(full_times, currentOffset, piece.parts[part_num].id, -pitch_num)
                    
                currentOffset += 0.5

            # if currentOffset > this_note_offset,
            # it skipped over a sixteenth note!
            # print that sixteenth out, save lastnote, and move one
            # if currentOffset > this_note_offset: 
            #    print "exit, currentOffset > this_note_offset"
            #    print currentOffset, this_note_offset, piece.parts[part_num].id
            #    sys.exit()

            # so we now know that currentOffset == this_noteOffset
            if type(n) is note.Note:
                file_out.write(str(n.offset + offset) + '\t' + str(n.midi) + '\t' + piece.parts[part_num].id + '\n')
                full_times = addToDict(full_times, n.offset + offset, piece.parts[part_num].id, n.midi)
                # print str(n.offset + offset) + '\t' + str(n.midi) + '\t' + piece.parts[part_num].id + '\n'
                lastPitch = [n.midi]
            elif type(n) is chord.Chord:
            # we know this is a chord, examine each note within
                lastPitch = []
                if piece.parts[part_num].id == "AddedChords":
                    # continue
                    #rn = roman.romanNumeralFromChord(n, SONG_KEY)
                    #rn = rn.figure

                    rn = n.root().name + n.quality
                    file_out.write(str(n.offset + offset) + '\t' + str(rn) + '\t' + piece.parts[part_num].id + '\n')
                    addToDict(full_times, n.offset + offset, piece.parts[part_num].id, rn)
                    lastPitch = [rn]
                else:                    
                    for pitch in n.pitches: 
                        file_out.write(str(n.offset + offset) + '\t' + str(pitch.midi) + '\t' + piece.parts[part_num].id + '\n')
                        full_times = addToDict(full_times, n.offset + offset, piece.parts[part_num].id, pitch.midi)
                        lastPitch.append(pitch.midi)
                        break
            elif type(n) is note.Rest:
                file_out.write(str(n.offset + offset) + '\t' + '1000' + '\t' + piece.parts[part_num].id + '\n')
                full_times = addToDict(full_times, n.offset + offset, piece.parts[part_num].id, 1000)
                lastPitch = [1000]
            else:
                print("unknown type")
                sys.exit()

            # prepare to start examining new notes
            currentOffset += 0.5

    file_out.close()

    this_tuple_list = full_times.get(offset)
    while this_tuple_list:

        
        # for t in this_tuple_list:
            
        print(str(offset) + ", " + str(this_tuple_list[0]) + ", " + str(this_tuple_list[1]) + ", " + str(this_tuple_list[2]) + ", " + str(this_tuple_list[3]) + ", " + str(this_tuple_list[4]))
        # print offset, this_tuple_list[0], this_tuple_list[1], this_tuple_list[2], this_tuple_list[3]
        
        offset += 0.5
        this_tuple_list = full_times.get(offset)

    print "exiting"
    sys.exit()
    # print full_times

    offset = 0 # absolute index into full_times
    this_measure_num = 0
    all_measures = []
    this_measure = []

    beats = [] # list of ( lists of (tuples) )

    
    this_tuple_list = full_times.get(offset)
    while this_tuple_list:

        # check if entered new measure
        new_measure = (int) (offset / 4)
        if new_measure > this_measure_num:
            this_measure_num = new_measure

            # save old "this_measure"
            all_measures.append(this_measure)
            # print this_measure
            # print " committed to all_measures -------------"

            # initialize new "this_measure"
            this_measure = []

        # add the appropriate time
        this_beat = this_tuple_list
        new_time = offset % 4 + 1
        this_beat.append(toPair(("time", new_time)))        

        this_measure.append(this_beat)
        # print this_measure
        # print " adding beat to this measure -------------"

        # keep checking each quarter note        
        offset += 0.5
        this_tuple_list = full_times.get(offset)

    
    
    file_out.close()
    
    #print "-----"
    #print all_measures[0]
    #print "-----"
    #print all_measures[1]
    #print "-----"

    # ADDS EXTRA COMMA TO 3RD TO LAST LINE
    print '{\n"measures": ['
    for measure in all_measures:
        print '{"beats":\n['
        print ('{' +
        '},\n{'.join([', '.join(str(n)) for n in measure]) + '}')
        print ']\n},'
    print ']\n}'
    
    final_measures = []
    for measure in all_measures:
        final_measures.append(("beats", measure))

    final_measures

    final_final_measure = ("measures", final_measures)

    # print final_final_measure
    

# actually reads chorales and stuff
def get_chorales():
    # read piece
    for workName in corpus.getBachChorales():

        # score object
        try:
            work = converter.parse(workName)
            print(workName + " exists")
            work = transpose(work) # jbocarsly addition, transpose
            work = add_chords(work)
            print("transposed!")
        except:
            print(workName + " hit exception continue")
            continue
    
        # name
        names = workName.split('\\')
        filename = names[len(names) - 1]
    
        # new name
        newfilename = filename + '.keynorm.raw'

        TS = work.getTimeSignatures()[0]
        ratioStr = "TS" + TS.ratioString.replace('/', '-')

        newfilename = ratioStr + "." + newfilename

        # reads chorales and does stuff with them
        offset = 0
        valid = 1
        try:
            measure_offsets = work.measureOffsetMap().keys()
            measure_offsets.remove(0.0)
            offset = min(measure_offsets)
            if ratioStr == "TS4-4":                
                offset = 4 - offset
            else:
                valid = 0            
        except Exception:
            print "offsetmap broken"
            valid = 0
        
        # output before the storm
        # print work, filename, newfilename
    
        # run through raw
        if valid == 1:
            write_raw(work, newfilename, offset)
        else:
            print("UNSUPPORTED time signature" + workName)
        # sys.exit()

    print("done!")

# read chorales
def read_chorales():
    # read piece
    for workName in corpus.getBachChorales():

        # score object
        try:
            work = converter.parse(workName)
            print(workName + " exists")
        except:
            print("hit exception continue")
            continue
    
        # name
        names = workName.split('\\')
        filename = names[len(names) - 1]
    
        # new name
        newfilename = filename + '.raw'

        # print out TS values
        TS = work.getTimeSignatures()[0]
        ratioStr = "TS" + TS.ratioString.replace('/', '-')        
        print ("signature: " + ratioStr)

        # reads chorales and does stuff with them
        offset = 0
        valid = 1
        try:
            measure_offsets = work.measureOffsetMap().keys()
            measure_offsets.remove(0.0)
            offset = min(measure_offsets)
            if ratioStr == "TS4-4":                
                offset = 4 - offset
            else:
                valid = 0            
        except Exception:
            print "offsetmap broken"
            valid = 0

        output_map = work.measureOffsetMap()
        output_map = sorted(output_map)
        print offset, output_map[0], output_map[1]

        # output before the storm
        # print work, filename, newfilename

    print("done!")

# old experiments
def old_parsing():
    filename='bach/bwv7.7'
    stdout = sys.stdout
    piece = corpus.parse(filename)
    newfilename=filename + '.raw'

    write_raw(piece, newfilename)

    filename='bach/bwv70.11'
    piece = corpus.parse(filename)
    newfilename=filename + '.raw'

    write_raw(piece, newfilename)

    sys.stdout = stdout

def get_chorale(target_chorale):
    # read piece
    for workName in corpus.getBachChorales():
               
        # score object
        try:
            work = converter.parse(workName)
            print(workName + " exists!")
        except Exception as ex:
            print(workName + "DNE: " + type(ex).__name__)            
    
        # name
        names = workName.split('\\')
        filename = names[len(names) - 1]
        print filename
        
        if filename == target_chorale:
            return work
    
    return None

# jbocarlsy code to transpose. Sample usage:
# s = corpus.parse('bach/bwv66.6')
#   s.show()
#   print "original:", s.analyze('key')
#   snew = transpose(s)
#   snew.show() 
#   print "new", snew.analyze('key')
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

def add_chords(s):
  '''given a stream and the key its in, adds a new part called 'chords' which has the closed form of the chords
  make by the other parts at the latin name of the chords as lyrics to that track'''
  sChords = s.chordify()
  sChords.id = 'AddedChords'
  s.insert(0, sChords)
  for c in sChords.flat.getElementsByClass('Chord'):
    c.closedPosition(forceOctave=4, inPlace=True)
  return s
    
# main
def main():
    work = corpus.parse('bach/bwv227.11.mxl')
    #work = converter.parse("C:\\Python27\\lib\\site-packages\\music21\\corpus\\bach\\bwv227.11.mxl")
    work = transpose(work) # jbocarsly addition, transpose
    work = add_chords(work)
    # work.show()
    write_raw(work, "mystuff", 0)
    # get_chorales()
    # read_chorales()

# stuff
if __name__ == "__main__":
    main()
