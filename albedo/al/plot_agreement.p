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
#set yrange[0.0:0.18]
#set ytics( '' 0.90, 0.95, 1.0, 1.05, '' 1.10 )
#set arrow from 1e-3,1.0 to 10.0,1.0 nohead lc rgb"red" lt 2 lw 1
set key center
plot "combined_reflections.txt" using 1:2:3 with errorbars title "MCNP",\
     "combined_reflections.txt" using 1:4:5 with errorbars title "FACEMC-ACE",\
     "combined_reflections.txt" using 1:6:7 with errorbars title "FACEMC-Native",\
     "combined_reflections.txt" using 1:8:9 with errorbars title "FACEMC-Moments",\
     "combined_reflections.txt" using 1:10 title "Experimental",
replot
unset key
unset multiplot
