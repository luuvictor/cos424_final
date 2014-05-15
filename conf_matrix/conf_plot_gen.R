#Just change the fields accessed to generate plots

setwd('/Users/Josh/cos424_final/conf_matrix/')
df = read.csv('concat_BEST.csv', as.is=T)
conf <- table(df[,c('original_chord', 'simple6CHORD')])
#conf <- table(df[,c('original_chord', 'viterbi8_chords')])

conf

conf.props <- aaply(conf, 1, function (x) x / sum(x))
print(conf.props)
plot.confusion(conf.props)
