import viterbi, viterbi4, viterbi8, simple6, simple1, to_array

all_chorales = to_array.read_all_csv_chorales()

file1='MAJORbwv411.mxl.csv'
file2='MAJORbwv430.mxl.csv'


simple6.generate_alto(all_chorales, file1)
simple1.generate_alto(all_chorales, file1)
#viterbi4.generate_alto(all_chorales, file1)
viterbi8.generate_alto(all_chorales, file1)


simple1.generate_alto(all_chorales, file2)
simple6.generate_alto(all_chorales, file2)
viterbi4.generate_alto(all_chorales, file2)
viterbi8.generate_alto(all_chorales, file2)