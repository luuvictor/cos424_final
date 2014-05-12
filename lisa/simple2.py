from pdf2 import *
import sys, os

def simpleModel(music, model):
	M = int(len(music.keys())/2.0)
	cnt = 0
	seq=[]

	max_prob=float("-inf")
	best_a=-1

	for a in ALTO_RANGE:
		chord=music[0][CHORD]
		soprano=abs(int(music[0][SOPRANO]))
		p=model[ALTO](a, {SOPRANO:soprano})

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
			soprano=int(music[m][SOPRANO])
			alto_prev = seq[len(seq)-1]
			p=model[ALTO](a, {SOPRANO:soprano})
			if p > max_prob:
				max_prob=p
				best_a=a
		
		if best_a == 46:
			cnt += 1
			best_a = soprano
		seq.append(best_a)
	print "cnt = ", cnt
	return seq

def generate_alto(all_chorales, filename):
	DIR = 'simple2'

	triplets_dict={}
	model=getPDF(triplets_dict)
	triplets=[]
	for key in triplets_dict:
	    triplets.append(triplets_dict[key])

	if not os.path.exists(DIR):
		os.mkdir(DIR)
	stitchFilename=DIR+'/'+filename[5:]
	
	with open(stitchFilename, 'w') as f:
		f.write(str(simpleModel(all_chorales[filename], model)))


"""
for chorale in all_chorales:
    print Viterbi(all_chorales[chorale], model, triplets)
    break
"""

