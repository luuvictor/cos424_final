import viterbi4, viterbi8, simple6, simple1, simple2, simple3, simple7, to_array

all_chorales = to_array.read_all_csv_chorales()

file1='MAJORbwv411.mxl.csv'
file2='MAJORbwv430.mxl.csv'

# Simple model
simple2.generate_alto(all_chorales, file1)

# Simple model 2
simple3.generate_alto(all_chorales, file1)

# Intermediate model 1
simple1.generate_alto(all_chorales, file1)

# Intermediate model 2
simple7.generate_alto(all_chorales, file1)

# Intermediate model 3
simple6.generate_alto(all_chorales, file1)

# Viterbi without links between alto notes
viterbi4.generate_alto(all_chorales, file1)

# Viterbi with links between alto notes
viterbi8.generate_alto(all_chorales, file1)
