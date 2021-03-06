#!/usr/bin/python -tt

import viterbi, viterbi4, viterbi8, simple6, simple1, simple2, simple3, simple7, to_array, pdf, pdf1, pdf2, pdf3, pdf4, pdf6, pdf7, pdf8
import os, sys



  
def main(): 
  madrigal_name = 'MAJORmadrigal.4.15.mxl.csv'    
  #i know this is weird i'm sorry. The infile has the .mxl.csv filenames!
  mode = madrigal_name[:5]
  cn = madrigal_name[5:-8]
  
  print mode, cn
  try:
    run_all_predictions(cn, mode)    
    print 'success running:   ' + cn
  except: 'failure running:   ' + cn

# MODE must be 'MAJOR' or 'MINOR'
def run_all_predictions(chorale_name,MODE):

  all_chorales = to_array.read_all_csv_chorales()

  filename= MODE + chorale_name + '.mxl.csv'
  
  
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
      f.write(str(viterbi.generate_alto(model, all_chorales, file1)))
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

def predict_viterbi9(chorale_name,MODE): #predicts for viterbi9, the new eighth note model
  
  all_chorales = to_array.read_all_csv_chorales()
  filename= MODE + chorale_name + '.mxl.csv'
  
  DIR = 'viterbi9'
  triplets_dict={}
  model=pdf9.getPDF(triplets_dict)
  triplets=[]
  for key in triplets_dict:
      triplets.append(triplets_dict[key])
      
  if not os.path.exists(DIR):
      os.mkdir(DIR)
  stitchFilename=DIR+'/'+filename[5:]
  print stitchFilename
  with open(stitchFilename, 'w') as f:
    f.write(str(viterbi8.generate_alto(model, triplets, all_chorales, filename)))
  

if __name__ == '__main__':
  main()