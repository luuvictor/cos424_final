import viterbi, viterbi4, viterbi8, viterbi9, simple6, simple1, simple2, simple3, simple7, to_array, pdf, pdf1, pdf2, pdf3, pdf9, pdf4, pdf6, pdf7, pdf8, os, sys

all_chorales = to_array.read_all_csv_chorales()

filename='MAJORbwv411.mxl.csv'


"""
DIR = 'viterbi'
triplets_dict={}
model=pdf.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])
if not os.path.exists(DIR):
	os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]
with open(stitchFilename, 'w') as f:
		f.write(str(viterbi.generate_alto(model, triplets, all_chorales, file1)))
"""

DIR = 'viterbi9'
triplets_dict={}
model=pdf9.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])
if not os.path.exists(DIR):
    os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]
with open(stitchFilename, 'w') as f:
		f.write(str(viterbi9.generate_alto(model, triplets, all_chorales, filename)))

"""
# Simple model
DIR = 'simple2'
triplets_dict={}
model=pdf2.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])

if not os.path.exists(DIR):
	os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]

with open(stitchFilename, 'w') as f:
		f.write(str(simple2.generate_alto(model, all_chorales, filename)))




# Simple model 2
DIR = 'simple3'
triplets_dict={}
model=pdf3.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])

if not os.path.exists(DIR):
	os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]

with open(stitchFilename, 'w') as f:
	f.write(str(simple3.generate_alto(model, all_chorales, filename)))



# Intermediate model 1
DIR = 'simple1'
triplets_dict={}
model=pdf1.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])
if not os.path.exists(DIR):
	os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]

with open(stitchFilename, 'w') as f:
	f.write(str(simple1.generate_alto(model, all_chorales, filename)))


# Intermediate model 2
DIR = 'simple7'
triplets_dict={}
model=pdf7.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])
if not os.path.exists(DIR):
	os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]

with open(stitchFilename, 'w') as f:
	f.write(str(simple7.generate_alto(model, all_chorales, filename)))


# Intermediate model 3
DIR = 'simple6'
triplets_dict={}
model=pdf6.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])
if not os.path.exists(DIR):
	os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]

with open(stitchFilename, 'w') as f:
	f.write(str(simple6.generate_alto(model, all_chorales, filename)))


# Viterbi without links between alto notes
DIR = 'viterbi4'
triplets_dict={}
model=pdf4.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])

if not os.path.exists(DIR):
    os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]
with open(stitchFilename, 'w') as f:
	f.write(str(viterbi4.generate_alto(model, triplets, all_chorales, filename)))


# Viterbi with links between alto notes
DIR = 'viterbi8'
triplets_dict={}
model=pdf8.getPDF(triplets_dict)
triplets=[]
for key in triplets_dict:
    triplets.append(triplets_dict[key])
if not os.path.exists(DIR):
    os.mkdir(DIR)
stitchFilename=DIR+'/'+filename[5:]
with open(stitchFilename, 'w') as f:
	f.write(str(viterbi8.generate_alto(model, triplets, all_chorales, filename)))
"""
