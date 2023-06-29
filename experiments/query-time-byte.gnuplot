set output 'query-time-byte.pdf'
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
set style function linespoints
plot "./query-time-byte/8byte.dat" using 1:2 title "8 Bytes" with linespoints linestyle 1, \
     "./query-time-byte/128byte.dat" using 1:2 title "128 Bytes" with linespoints linestyle 2, \
     "./query-time-byte/1024byte.dat" using 1:2 title "1024 Bytes" with linespoints linestyle 3
