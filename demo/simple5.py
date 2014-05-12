from pdf5 import *

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

		p=model[ALTO](a, {CHORD:chord})
		
		if p > max_prob:
			max_prob=p
			best_a=a
	seq.append(best_a)

	for m in range(1, M+1):
		max_prob=float("-inf")
		best_a=-1

		for a in ALTO_RANGE:
			
			chord=music[m][CHORD]
			soprano=int(music[m][SOPRANO])
			tenor=abs(int(music[m][TENOR]))
			bass=abs(int(music[m][BASS]))

			alto_prev = seq[len(seq)-1]
			p=model[ALTO](a, {CHORD:chord})
			if p > max_prob:
				max_prob=p
				best_a=a
		
		if best_a == 46:
			cnt += 1
			best_a = soprano
		seq.append(best_a)
	print "cnt = ", cnt
	return seq

print simpleModel(all_chorales['bwv436.mxl.csv'], model)


#print Viterbi(all_chorales['bwv_test.csv'], model, triplets)
"""
for chorale in all_chorales:
    print Viterbi(all_chorales[chorale], model, triplets)
    break
"""

