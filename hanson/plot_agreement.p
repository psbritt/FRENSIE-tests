set terminal post eps enh color
set terminal postscript eps enhanced
set output "plot_angular_dist.eps"
set title "15.7 MeV Electron Angular Distribution from a 9.658 {/Symbol m}m Gold Foil"
set tmargin at screen 0.8
set bmargin at screen 0.1
set lmargin at screen 0.12
set rmargin at screen 0.95
set format x "%3.2e"
set format y "%3.3f"
set xlabel "Angle (Degree)"
set ylabel "#/Square Degree"
set xrange[0.0:30.0]
#set yrange[0.0:0.18]
#set ytics( '' 0.90, 0.95, 1.0, 1.05, '' 1.10 )
#set arrow from 1e-3,1.0 to 10.0,1.0 nohead lc rgb"red" lt 2 lw 1
#set key outside top center
plot "computational_results.txt" using 1:2:3 with errorbars title "MCNP",\
     "computational_results.txt" using 1:4:5 with errorbars title "FACEMC-ACE"
#plot "computational_results.txt" using 1:4:5 with errorbars title "FACEMC-ACE",\
#     "computational_results.txt" using 1:6:7 with errorbars title "FACEMC-LinLin",\
#     "computational_results.txt" using 1:8:9 with errorbars title "FACEMC-LinLog" 
unset multiplot
