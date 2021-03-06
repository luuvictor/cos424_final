from pdf import *

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

	seq=[]

	max_prob=float("-inf")
	best_a=-1

	for a in ALTO_RANGE:
		chord=music[0][CHORD]
		soprano=abs(int(music[0][SOPRANO]))
		p=model[ALTO](a, {CHORD:chord, SOPRANO:soprano})

		#print "chord: ", chord
		#print "soprano: ", soprano
		#print a, p
		
		if p > max_prob:
			max_prob=p
			best_a=a
	seq.append(best_a)

	for m in range(1, M):
		max_prob=float("-inf")
		best_a=-1

		for a in ALTO_RANGE:
			
			chord=music[m][CHORD]
			soprano=abs(int(music[m][SOPRANO]))
			alto_prev = seq[len(seq)-1]
			p=model[ALTO](a, {CHORD:chord, SOPRANO:soprano, ALTO:alto_prev})
			if p > max_prob:
				max_prob=p
				best_a=a
		seq.append(best_a)
	return seq

print simpleModel(all_chorales['bwv437.mxl.csv'], model)

#print Viterbi(all_chorales['bwv_test.csv'], model, triplets)
"""
for chorale in all_chorales:
    print Viterbi(all_chorales[chorale], model, triplets)
    break
"""

