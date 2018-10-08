set terminal post eps enh color
set output "plot_coef.eps"
set title "Reflection Coef for Al-slab Electron Albedo Problem"
set multiplot layout 2,1 rowsfirst
set tmargin at screen 0.47
set bmargin at screen 0.1
set lmargin at screen 0.12
set rmargin at screen 0.95
set format x "%3.2e"
set format y "%3.2f"
set xlabel "Energy (MeV)"
set ylabel "Reflection Coef"
set xrange[1.0E-04:6.3E-02]
#set yrange[0.0:0.18]
#set ytics( '' 0.90, 0.95, 1.0, 1.05, '' 1.10 )
#set arrow from 1e-3,1.0 to 10.0,1.0 nohead lc rgb"red" lt 2 lw 1
set key outside top center
plot "combined_reflections.txt" using 1:2:3 with errorbars title "MCNP",\
     "combined_reflections.txt" using 1:4:5 with errorbars title "ACE",\
     "combined_reflections.txt" using 1:6:7 with errorbars title "LinLog",\
     "combined_reflections.txt" using 1:10:11 with errorbars title "LinLin",\
     "experimental_reflections_2.txt" using 1:2 title "Neubert",\
     "experimental_reflections_2.txt" using 1:3 title "Bishop",\
     "experimental_reflections_2.txt" using 1:4 title "Joy Ref. 2",\
     "experimental_reflections_2.txt" using 1:5 title "Joy Ref. 4",\
     "experimental_reflections_2.txt" using 1:6 title "Joy Ref. 5",\
     "experimental_reflections_2.txt" using 1:7 title "Joy Ref. 6",\
     "experimental_reflections_2.txt" using 1:8 title "Joy Ref. 14",\
     "experimental_reflections_2.txt" using 1:9 title "Joy Ref. 15",\
     "experimental_reflections_2.txt" using 1:10 title "Joy Ref. 22",\
     "experimental_reflections_2.txt" using 1:11 title "Joy Ref. 35",\
     "experimental_reflections_2.txt" using 1:12 title "Joy Ref. 68",\
     "experimental_reflections_2.txt" using 1:13 title "Joy Ref. 106",\
     "experimental_reflections_2.txt" using 1:14 title "Joy Ref. 107"
unset multiplot
