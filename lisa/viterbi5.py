# things that need to be filled in or changed are marked with "#!", search for them.
# in my comments, I refer to a list of lists as a list of "columns"
# REMEMBER TO USE LOG PROBABILITIES
import random, math
from pdf5 import *

# "model" is your object containing all probability distributions, I haven't called it anywhere below
# soparno, tenor, bass are the GIVEN voices, we are trying to predict the alto
def Viterbi(music, model, triplets):
    M = int(len(music.keys())/2.0) # M is the length of the piece that we are given
    # ASSUMES THAT soprano, tenor, bass ALL HAVE THE SAME LENGTH, MIGHT NEED TO TWEAK
    
    #!
    # chords = model.getChords() # list of all chords
    chords = CHORD_RANGE
    # chords = [4, 7] # alternatively, if you have all the chords indexed already
    
    #!
    # notes = model.getAltoNotes() # list of all possible notes for the alto
    notes = ALTO_RANGE # you mentioned that they would be strings, so I made them strings here
    # notes = [60, 62, 64, 72] # alternatively, if you have the notes indexed already
    
    #!
    # list of triplets (chord, current alto note, previous alto eighth note), if you haven't done this already
    # this may vary if you have a fancy way of accessing... but the rest of the code relies on having this list of all triplets
    """
    triplets = []
    for chord in chords:
        for note1 in notes:
            for note2 in notes:
                triplets.append([chord, note1, note2])
    """
    # for i in range(0,len(triplets)): print triplets[i]
    
    #####
    # these are the matrices of dimension "len(triplets) by M" 
    bestPrevTriplet = []
    maxProb = []
    
    ##### initialization: "time = 0", i.e., first beat
    bestPrevTriplet.append([-1]*len(triplets)) # adds [-1,-1,-1,...] as the first column of bestPrevState, ignore this
    initProb = [] # this will be the first column of maxProb
    for i in range(0,len(triplets)): # for each triplet...
        # REMEMBER TO USE LOG PROBABILITIES
        #! calculate base case here!
        triplet = triplets[i]

        time=0
        chord=triplet[0]
        soprano=music[time][SOPRANO]
        alto=triplet[1]
        #alto1=triplet[2]
        tenor=music[time][TENOR]
        bass=music[time][BASS]

        pq = model[CHORD](chord, {TIME:time})
        pa = model[SOPRANO](soprano, {CHORD:chord})
        pb = model[ALTO](alto, {CHORD:chord, SOPRANO:soprano})
        pc = model[TENOR](tenor, {CHORD:chord, SOPRANO:soprano})
        pd = model[BASS](bass, {CHORD:chord})

        prob = pq+pa+pb+pc+pd


        # access the actual triplet by using "triplets[i]".
        # get the model probabilities corresponding this triplet and all the given voices. note that this is "time = zero," i.e., the first beat
        initProb.append(prob) # build column of probabilities

    maxProb.append(initProb) # first column of maxProb
    #print "maxProb = ", maxProb

    #####    
    for m in range(1,M): # for each subsequent beat of the piece... (m is "time" but I don't want to confuse it with the "time" random variable)
        # this will be the mth columns of maxProb and bestPrevTriplet
        maxProbCol = [];
        bestPrevTripletCol = [];
        
        for i in range(0,len(triplets)): # for each triplet at time m...
            #print "outer loop ", triplets[i]
            max = float("-inf") # keep track of max prob, initialize to negative infinity
            prevTriplet = -1 # keep track of best prev state

            print ""
            print "m = ", m

            time= m % 4
            chord = triplets[i][0]
            alto=triplets[i][1]
            #alto1=triplets[i][2]

            soprano=music[m][SOPRANO]
            soprano1=music[m-.5][SOPRANO]
            tenor=music[m][TENOR]
            tenor1=music[m-.5][TENOR]
            bass=music[m][BASS]

            bass1=music[m-.5][BASS]

            soprano_prev=music[m-1][SOPRANO]
            tenor_prev = music[m-1][TENOR]
            bass_prev = music[m-1][BASS]

            pa = model[SOPRANO](soprano, {SOPRANO:soprano_prev, CHORD:chord})
            pc = model[TENOR](tenor, {TENOR:tenor_prev, CHORD:chord})
            pd = model[BASS](bass, {BASS:bass_prev, CHORD:chord})

            #pa1= model[SOPRANO1](soprano1, {SOPRANO1:soprano_prev, SOPRANO:soprano})
            #pc1= model[TENOR1](tenor1, {TENOR1:tenor_prev, TENOR:tenor})
            #pd1= model[BASS1](bass1, {BASS1:bass_prev, BASS:bass})

            for j in range(0,len(triplets)): # for each triplet at time m-1
                #print "inner loop ", triplets[j]
                # REMEMBER TO USE LOG PROBABILITIES
                #! do inductive step here

                chord_prev = triplets[j][0]
                alto_prev=triplets[j][1]

                pq = model[CHORD](chord, {CHORD:chord_prev, TIME:time})
                pb = model[ALTO](alto, {CHORD:chord})
                #pb1= model[ALTO1](alto1, {ALTO1:alto_prev, ALTO:alto})

                #prob = pq+pa+pb+pc+pd+pa1+pb1+pc1+pd1+maxProb[m-1][j]
                prob = pq+pb+maxProb[m-1][j]

                #print "prob = ", prob

                #prob = maxProb[m-1][j] + math.log(random.random()) + math.log(random.random()) 
                
                # maxProb[m-1][j] is the "alpha" term from our calculations,
                # need to calculate everything else using the model
                # can access stuff using triplets[i] (triplet at time m) and triplets[j] (triplet at time m-1)
                
                # keep track of best one so far
                if prob > max:
                    max = prob
                    prevTriplet = j
            
            # build columns
            #print "max = ", max
            maxProbCol.append(max+pa+pc+pd)
            bestPrevTripletCol.append(prevTriplet)
        
        # append columns to big matrix
        #print maxProbCol
        maxProb.append(maxProbCol)
        bestPrevTriplet.append(bestPrevTripletCol)
    
    ##### take final maximum
    seq = []
    max = float("-inf")
    lastTriplet = -1
    # find the triplet that maximizes last column of maxProb
    for i in range(0,len(triplets)):
        if maxProb[M-1][i] > max:
            max = maxProb[M-1][i]
            lastTriplet = i
    seq.insert(0,lastTriplet) # insert into front of sequence
    
    # backtrack to recover sequence
    for m in range(0,M-1):
        seq.insert(0,bestPrevTriplet[m+1][seq[0]]) # find what the best previous triplet was, and insert it into the front of seq
    
    # convert triplet index to actual triplet name
    for i in range(0, len(seq)):
        seq[i] = triplets[seq[i]]
    return seq


triplets_dict={}
model=getPDF(triplets_dict)
print "len(triplets) = ", len(triplets_dict)
#print triplets_dict

triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])

all_chorales = to_array.read_all_csv_chorales()
print Viterbi(all_chorales['bwv_test.csv'], model, triplets)
"""
for chorale in all_chorales:
    print Viterbi(all_chorales[chorale], model, triplets)
    break
"""



#print Viterbi([1,5,4],[7,5,3],[6,4,2],["hello", "I is probability distribution"])

