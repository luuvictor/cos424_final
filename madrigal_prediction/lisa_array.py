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

SOPRANO_RANGE = range(52, 86)
ALTO_RANGE = range(46, 81)
TENOR_RANGE = range(41, 76)
BASS_RANGE = range(28, 70)
CHORD_RANGE = ["i"]
RANGE = [SOPRANO_RANGE, ALTO_RANGE, TENOR_RANGE, BASS_RANGE, CHORD_RANGE]

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
def addCount(C, mxlname):
	work = to_array.getArray(mxlname)
	times = to_array.corpus_to_array(work, "mystuff", 0)


	my_offset = 0
	cur = times.get(my_offset)

	D = [{}, {}, {}, {}, {}, {}, {}, {}, {}]

	# initial (t = 0)
	# SOPRANO
	child = cur[SOPRANO]
	parents = {CHORD:cur[CHORD]}
	addToDict(D[SOPRANO], child, parents)

	# ALTO
	child = cur[ALTO]
	parents = {CHORD:cur[CHORD], SOPRANO:cur[SOPRANO]}
	addToDict(D[ALTO], child, parents)

	# TENOR
	child = cur[TENOR]
	parents = {CHORD:cur[CHORD], SOPRANO:cur[SOPRANO]}
	addToDict(D[TENOR], child, parents)

	# BASS
	child = cur[BASS]
	parents = {CHORD:cur[CHORD]}
	addToDict(D[BASS], child, parents)
	
	# CHORD
	child = cur[CHORD]
	parents = {TIME:offsetToTime(my_offset)}
	addToDict(D[CHORD], child, parents)

	my_offset += 1
	cur = times.get(my_offset)
	prev = times.get(my_offset-1)
	btwn = times.get(my_offset-.5)

	while cur:

	    
	    # SOPRANO
		child = cur[SOPRANO]
		parents = {SOPRANO:prev[SOPRANO], CHORD:cur[CHORD]}
		addToDict(D[SOPRANO], child, parents)

		# ALTO
		child = cur[ALTO]
		parents = {ALTO:prev[ALTO], CHORD:cur[CHORD], SOPRANO:cur[SOPRANO]}
		addToDict(D[ALTO], child, parents)

		# TENOR
		child = cur[TENOR]
		parents = {TENOR:prev[TENOR], CHORD:cur[CHORD], SOPRANO:cur[SOPRANO]}
		addToDict(D[TENOR], child, parents)

		# BASS
		child = cur[BASS]
		parents = {BASS:prev[BASS], CHORD:cur[CHORD]}
		addToDict(D[BASS], child, parents)

		# SOPRANO1
		child = btwn[SOPRANO]
		parents = {SOPRANO1:prev[SOPRANO], SOPRANO:cur[SOPRANO]}
		addToDict(D[SOPRANO1], child, parents)

		# ALTO1
		child = btwn[ALTO]
		parents = {ALTO1:prev[ALTO], ALTO:cur[ALTO]}
		addToDict(D[ALTO1], child, parents)

		# TENOR1
		child = btwn[TENOR]
		parents = {TENOR1:prev[TENOR], TENOR:cur[TENOR]}
		addToDict(D[TENOR1], child, parents)

		# BASS1
		child = btwn[BASS]
		parents = {BASS1:prev[BASS], BASS:cur[BASS]}
		addToDict(D[BASS1], child, parents)

		# CHORD
		child = cur[CHORD]
		parents = {CHORD:prev[CHORD], TIME:offsetToTime(my_offset)}
		addToDict(D[CHORD], child, parents)

		# preparation for the next iteration
		my_offset += 1
		cur = times.get(my_offset)
		prev = times.get(my_offset-1)
		btwn = times.get(my_offset-.5)
	
	"""
	print "SOPRANO: ", D[SOPRANO]
	print ""
	print "ALTO: ", D[ALTO]
	"""

	"""
	d=[{}]*9
	for attr in range(9):
		print "before =  ", d[attr]
		print ""
		print "D[attr] = ", D[attr]
		print ""
		d[attr]=dictToCounter(D[attr])
		print "after = ", d[attr]
		print "----------------------------------"
		"""

	for attr in range(9):
		d = dictToCounter(D[attr])
		for key in d:
			if key in C[attr]:
				C[attr][key] += d[key]
			else:
				C[attr][key] = d[key]


"""
Print mxlname file to stdout.
"""
def printXML(mxlname):
	work = to_array.getArray(mxlname)
	times = to_array.corpus_to_array(work, "mystuff", 0)

	my_offset=0
	cur = times.get(my_offset)

	while cur:
		print my_offset, cur[SOPRANO], cur[ALTO], cur[TENOR], cur[BASS], cur[CHORD]
		my_offset += .5
		cur = times.get(my_offset)



"""
Return the pdf of D, which is a dictionary of counters
"""
def dictToPDF(D, attr):
	tot_cnt={}
	for parents in D:
		tot_cnt[parents] = 0.0
		#print "D[parents] = ", D[parents]
		for key in D[parents]:
			tot_cnt[parents] += D[parents][key]
		#for cnt in counter[parents]:
			#tot_cnt[parents] = tot_cnt[parents] + counter[parents][c]

	def pdf(child, parents):
		#tot_cnt = tot_cnt1.copy()
		p = getKey(parents)
		if p in tot_cnt:
			#return D[p][child]/tot_cnt[p]
			return math.log(D[p][child]/tot_cnt[p])
		else: # return uniform distribution
			#print "len = ", 1.0/len(RANGE[attr])
			return math.log(1.0/len(RANGE[attr]))
	return pdf

def getPDFarray(C):
	P=[]
	for attr in range(9):
		P.append(dictToPDF(C[attr], attr))
	return P

def getPDF(xmlfiles):
	# List of counters, indexed by attribute
	C= [{}, {}, {}, {}, {}, {}, {}, {}, {}]

	for xmlfile in xmlfiles:
		addCount(C, xmlfile)
	return getPDFarray(C)


xmlfiles = ['bach/bwv227.11.mxl']
p=getPDF(xmlfiles)

print p
#xmlfile='bach/bwv227.11.mxl'
#printXML(xmlfile)

print "log(1/34) = ", p[SOPRANO](76, {SOPRANO:79, CHORD:'Cminor'})

print "log(.3333) = ", p[SOPRANO](76, {SOPRANO:-81, CHORD:'Aminor'})
print "log(1) = ", p[ALTO]( 72, {ALTO:-72, CHORD:'Aminor', SOPRANO:76})



