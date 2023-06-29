set output 'cache-hit-rate.pdf'
set term pdfcairo font "Times New Roman,18"
set size ratio 0.75
set style fill solid
# set key left top
set key outside
set yrange [0:1]
set xlabel 'Caches Owned by NSs / Total Caches'
set ylabel 'Cache Hit Rate'
plot "./cache-hit-rate/result.dat" using 2:xtic(1) title "theoretical" with histograms linecolor "#2196F3", "" using 3 title "practical" with histograms linecolor "#66BB6A"
