from pdf7 import *
from os import listdir
import os
from to_array import *

triplets_dict={}
model=getPDF(triplets_dict)
#print "len(triplets) = ", len(triplets_dict)
#print triplets_dict

triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])


all_chorales = to_array.read_all_csv_chorales()

def simpleModel(music, model):
	M = int(len(music.keys())/2.0)
	cnt = 0
	seq=[]

	max_prob=float("-inf")
	best_a=-1

	for a in ALTO_RANGE:
		chord=music[0][CHORD]
		soprano=abs(int(music[0][SOPRANO]))
		tenor=abs(int(music[0][TENOR]))
		bass=abs(int(music[0][BASS]))

		p=model[ALTO](a, {SOPRANO:soprano, TENOR:tenor, BASS:bass})
		
		if p > max_prob:
			max_prob=p
			best_a=a
	seq.append(best_a)

	for m in range(1, M):
		max_prob=float("-inf")
		best_a=-1

		for a in ALTO_RANGE:
			
			chord=music[m][CHORD]
			soprano=int(music[m][SOPRANO])
			tenor=abs(int(music[m][TENOR]))
			bass=abs(int(music[m][BASS]))

			alto_prev = seq[len(seq)-1]
			p=model[ALTO](a, {SOPRANO:soprano, TENOR:tenor, BASS:bass})
			if p > max_prob:
				max_prob=p
				best_a=a
		
		if best_a == 46:
			cnt += 1
			best_a = soprano
		seq.append(best_a)
	print "cnt = ", cnt
	return seq

"""
music=""
for f in listdir(os.getcwd()):
	if f.find("bwv1.6") != -1:
		music=read_csv_to_array(f)
"""

music=all_chorales['MAJORbwv438.mxl.csv']
print simpleModel(music, model)


#print Viterbi(all_chorales['bwv_test.csv'], model, triplets)
"""
for chorale in all_chorales:
    print Viterbi(all_chorales[chorale], model, triplets)
    break
"""

