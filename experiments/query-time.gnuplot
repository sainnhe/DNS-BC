set output 'query-time.pdf'
set term pdfcairo font "Times New Roman,18"
set size ratio 0.75
set key outside
# set xrange [0:1000]
# set yrange [0:800]
set xlabel 'Query Time (ms)'
set ylabel 'Probability'
set style line 1 linewidth 1.5 linetype rgb "#E53935" pointtype 3 pointsize default pointinterval 100
set style line 2 linewidth 1.5 linetype rgb "#2962FF" pointtype 6 pointsize default pointinterval 100
set style function linespoints
plot "./query-time/hashmap.dat" using 1:2 title "HM" with linespoints linestyle 1, \
     "./query-time/blockchain.dat" using 1:2 title "BC" with linespoints linestyle 2
