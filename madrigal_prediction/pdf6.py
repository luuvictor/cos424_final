import to_array, math
from collections import Counter


"""
constants
"""
SOPRANO = 0
ALTO = 1
TENOR = 2
BASS = 3
CHORD = 4
SOPRANO1=5
ALTO1=6
TENOR1=7
BASS1=8
TIME = 9

SOPRANO_RANGE = range(52, 86)+[1000]
ALTO_RANGE = range(46, 81)+[1000]
TENOR_RANGE = range(41, 76)+[1000]
BASS_RANGE = range(28, 70)+[1000]
CHORD_RANGE = ['G#minor', 'D#diminished', 'Fother', 'C#other', 'D#minor', 'Cmajor', 'C#diminished', 'Bminor', 'B-augmented', 'Ddiminished', 'Dother', 'Eother', 'Gmajor', 'F#minor', 'Eminor', 'Dminor', 'E-major', 'Fmajor', 'Bother', 'Caugmented', 'Gdiminished', 'Cminor', 'Bdiminished', '1000', 'B-other', 'Cother', 'B-major', 'Adiminished', 'F#major', 'Faugmented', 'C#minor', 'Bmajor', 'F#other', 'Gother', 'Ediminished', 'Dmajor', 'G#other', 'A-major', 'Fminor', 'Amajor', 'Emajor', 'B-minor', 'D#other', 'Gaugmented', 'G#diminished', 'A#diminished', 'Gminor', 'F#diminished', 'A-other', 'Aother', 'Aminor']
SOPRANO_RANGE1 = SOPRANO_RANGE+[-1]
ALTO_RANGE1 = ALTO_RANGE+[-1]
TENOR_RANGE1 = TENOR_RANGE+[-1]
BASS_RANGE1 = BASS_RANGE+[-1]
RANGE = [SOPRANO_RANGE, ALTO_RANGE, TENOR_RANGE, BASS_RANGE, CHORD_RANGE, SOPRANO_RANGE, ALTO_RANGE, TENOR_RANGE, BASS_RANGE]

"""
 Add child to list d[parents]
"""
def addToDict(d, child, parents):
	p = getKey(parents)
	if not d.has_key(p):
		d[p]= []
	d[p].append(child)

"""
Convert cd into a dictionary of Counter objects.
"""
def dictToCounter(d):
	counters={}
	for parents in d:
		counters[parents]=Counter(d[parents])
	return counters


"""
Return key
"""
# d = {SOPRANO:74, ALTO:72}
def getKey(d):
	key=""
	for attr in range(10):
		if attr in d:
			key += str(d[attr])
	return key


"""
Parse s into int or float.
"""
def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def offsetToTime(offset):
	return offset % 4

"""
Add counts in mxlname to C.
"""
def addCount(C, mxlname, triplets):
	#work = to_array.getArray(mxlname)
	#times = to_array.corpus_to_array(work, "mystuff", 0)



	times = all_chorales[mxlname]

	my_offset = 0
	#print "mxlname = ", mxlname
	#print "times = ", times
	cur = times[my_offset]

	#print "len(time) = ", len(times)
	#print "len(cur) = ", len(cur)

	D = [{}, {}, {}, {}, {}, {}, {}, {}, {}]

	# initial (t = 0)
	# SOPRANO
	child = abs(int(cur[SOPRANO]))
	parents = {CHORD:cur[CHORD]}
	addToDict(D[SOPRANO], child, parents)

	# ALTO
	child = abs(int(cur[ALTO]))
	parents = {CHORD:cur[CHORD], SOPRANO:abs(int(cur[SOPRANO])), TENOR:abs(int(cur[TENOR])), BASS:abs(int(cur[BASS]))}
	addToDict(D[ALTO], child, parents)

	# TENOR
	child = abs(int(cur[TENOR]))
	parents = {CHORD:cur[CHORD], SOPRANO:abs(int(cur[SOPRANO]))}
	addToDict(D[TENOR], child, parents)

	# BASS
	child = abs(int(cur[BASS]))
	parents = {CHORD:cur[CHORD]}
	addToDict(D[BASS], child, parents)
	
	# CHORD
	child = cur[CHORD]
	parents = {TIME:offsetToTime(my_offset)}
	addToDict(D[CHORD], child, parents)

	my_offset += 1
	cur = times[my_offset]
	prev = times[my_offset-1]
	btwn = times[my_offset-.5]

	while cur:

		# triplet
		chord=cur[CHORD]
		alto=abs(int(cur[ALTO]))
		alto1=int(btwn[ALTO])
		triplets[getKey({CHORD:chord, ALTO:alto, ALTO1:alto1})] = [chord, alto, alto1]
		#print [chord, alto, alto1]

	    # SOPRANO
		child = abs(int(cur[SOPRANO]))
		parents = {SOPRANO:abs(abs(int(prev[SOPRANO]))), CHORD:cur[CHORD]}
		addToDict(D[SOPRANO], child, parents)

		# ALTO
		child = abs(int(cur[ALTO]))
		parents = {CHORD:cur[CHORD], SOPRANO:abs(int(cur[SOPRANO])), TENOR:abs(int(cur[TENOR])), BASS:abs(int(cur[BASS]))}
		addToDict(D[ALTO], child, parents)

		# TENOR
		child = abs(int(cur[TENOR]))
		parents = {TENOR:abs(int(prev[TENOR])), CHORD:cur[CHORD], SOPRANO:abs(int(cur[SOPRANO]))}
		addToDict(D[TENOR], child, parents)

		# BASS
		child = abs(int(cur[BASS]))
		parents = {BASS:abs(int(prev[BASS])), CHORD:cur[CHORD]}
		addToDict(D[BASS], child, parents)

		# SOPRANO1
		child = int(btwn[SOPRANO])
		parents = {SOPRANO1:abs(abs(int(prev[SOPRANO]))), SOPRANO:abs(int(cur[SOPRANO]))}
		addToDict(D[SOPRANO1], child, parents)

		# ALTO1
		child = int(btwn[ALTO])
		parents = {ALTO1:abs(int(prev[ALTO])), ALTO:abs(int(cur[ALTO]))}
		addToDict(D[ALTO1], child, parents)

		# TENOR1
		child = int(btwn[TENOR])
		parents = {TENOR1:abs(int(prev[TENOR])), TENOR:abs(int(cur[TENOR]))}
		addToDict(D[TENOR1], child, parents)

		# BASS1
		child = int(btwn[BASS])
		parents = {BASS1:abs(int(prev[BASS])), BASS:abs(int(cur[BASS]))}
		addToDict(D[BASS1], child, parents)

		# CHORD
		child = cur[CHORD]
		parents = {CHORD:prev[CHORD], TIME:offsetToTime(my_offset)}
		addToDict(D[CHORD], child, parents)

		# preparation for the next iteration
		my_offset += 1

		if my_offset not in times:
			break

		cur = times[my_offset]
		prev = times[my_offset-1]
		btwn = times[my_offset-.5]

	for attr in range(9):
		d = dictToCounter(D[attr])
		for key in d:
			if key in C[attr]:
				C[attr][key] += d[key]
			else:
				C[attr][key] = d[key]


"""
Return the pdf of D, which is a dictionary of counters
"""
def dictToPDF(D, attr):
	tot_cnt={}
	for parents in D:
		tot_cnt[parents] = 0.0
		for key in D[parents]:
			tot_cnt[parents] += D[parents][key]
	
	def pdf(child, parents):
		p = getKey(parents)
		
		if p in tot_cnt:
			if D[p][child] == 0:
				prob = 0
			else:
				#return D[p][child]/tot_cnt[p]
				prob = math.log(D[p][child]/tot_cnt[p])
		else:
			#return 1.0/len(RANGE[attr])
			#print "uniform"
			prob = math.log(1.0/len(RANGE[attr]))

		#print "log p(", child, "|", parents, ") = ", prob

		#print "parents = ", parents

		if p in tot_cnt:
			if D[p][child] == 0:
				return float("-inf")
			else:
				#return D[p][child]/tot_cnt[p]
				return math.log(D[p][child]/tot_cnt[p])
		else:
			#return 1.0/len(RANGE[attr])
			return math.log(1.0/len(RANGE[attr]))
	return pdf

def getPDFarray(C):
	P=[]
	for attr in range(9):
		P.append(dictToPDF(C[attr], attr))
	return P

def getPDF(triplets):
	global all_chorales
	all_chorales = to_array.read_all_csv_chorales()

	# List of counters, indexed by attribute
	C= [{}, {}, {}, {}, {}, {}, {}, {}, {}]
	
	for chorale in all_chorales:
		addCount(C, chorale, triplets)

	with open('counters', 'w') as f:
		f.write(str(C))
		f.close()

	return getPDFarray(C)


"""
Print mxlname file to stdout.
"""
def printXML(mxlname):
	times = all_chorales[mxlname]
	my_offset=0
	cur = times[my_offset]

	while cur:
		print my_offset, abs(int(cur[SOPRANO])), abs(int(cur[ALTO])), abs(int(cur[TENOR])), abs(int(cur[BASS])), cur[CHORD]
		my_offset += .5
		cur = times[my_offset]




#xmlfiles = ['bach/bwv227.11.mxl']
#p=getPDF(xmlfiles)

#print p
#xmlfile='bach/bwv227.11.mxl'
#printXML(xmlfile)

triplets_dict={}
p = getPDF(triplets_dict)

#for note in SOPRANO_RANGE:
#	print p[SOPRANO](note, {SOPRANO:76, CHORD:'Cmajor'})

#print p[SOPRANO](76, {SOPRANO:79, CHORD:'Cminor'})
#print p[SOPRANO](76, {SOPRANO:-81, CHORD:'Aminor'})
#print p[ALTO]( 72, {ALTO:-72, CHORD:'Aminor', SOPRANO:76})



