set output 'query-time-multiple.pdf'
set term pdfcairo font "Times New Roman,18"
set size ratio 0.75
set key outside
# set xrange [0:1000]
# set yrange [0:800]
set xlabel 'Query Time (ms)'
set ylabel 'Probability'
set style line 1 linewidth 1.5 linetype rgb "#E53935" pointtype 3 pointsize default pointinterval 100
set style line 2 linewidth 1.5 linetype rgb "#2962FF" pointtype 6 pointsize default pointinterval 100
set style line 3 linewidth 1.5 linetype rgb "#00e24c" pointtype 8 pointsize default pointinterval 100
set style line 4 linewidth 1.5 linetype rgb "#871be2" pointtype 12 pointsize default pointinterval 100
set style function linespoints
plot "./query-time-multiple/1.dat" using 1:2 title "1 NC" with linespoints linestyle 1, \
     "./query-time-multiple/3.dat" using 1:2 title "3 NC" with linespoints linestyle 2, \
     "./query-time-multiple/5.dat" using 1:2 title "5 NC" with linespoints linestyle 3, \
     "./query-time-multiple/10.dat" using 1:2 title "10 NC" with linespoints linestyle 4
