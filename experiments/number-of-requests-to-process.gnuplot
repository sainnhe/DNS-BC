set output 'number-of-requests-to-process.pdf'
set term pdfcairo font "Times New Roman,18"
set size ratio 0.75
# set key at graph 0.9, 0.8
set key outside
set xrange [0:1]
set yrange [0:1000]
set xlabel 'Caches Owned by NSs / Total Caches'
set ylabel 'Requests to Process'
set style line 1 linewidth 1.5 linetype rgb "#E53935" pointtype 3 pointsize default pointinterval 0.1
set style line 2 linewidth 1.5 linetype rgb "#2962FF" pointtype 6 pointsize default pointinterval 0.1
set style function linespoints
plot "./number-of-requests-to-process/result.dat" using 1:2 title "NSs" with linespoints linestyle 1, \
     "./number-of-requests-to-process/result.dat" using 1:3 title "RRs" with linespoints linestyle 2
