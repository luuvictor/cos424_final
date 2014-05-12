from pdf1 import *
import sys, os

all_chorales = to_array.read_all_csv_chorales()

def simpleModel(music, model):
	M = int(len(music.keys())/2.0)

	seq=[]

	max_prob=float("-inf")
	best_a=-1

	for a in ALTO_RANGE:
		chord=music[0][CHORD]
		soprano=abs(int(music[0][SOPRANO]))
		p=model[ALTO](a, {SOPRANO:soprano, CHORD:chord})
		
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
			#p=model[ALTO](a, {CHORD:chord, SOPRANO:soprano, ALTO:alto_prev}) # with link in ALTO
			p=model[ALTO](a, {CHORD:chord, SOPRANO:soprano}) # without link
			if p > max_prob:
				max_prob=p
				best_a=a
		seq.append(best_a)
	return seq

def generate_alto(all_chorales, filename):
	DIR = 'simple1'

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
filename='MAJORbwv430.mxl.csv'
print "# simple1.py"
print "stitchFilename='"+filename[5:]+"'"
print "notes = ", simpleModel(all_chorales[filename], model)
print "to_array.stitchIn(stitchFilename, notes)"


"""