reset
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_1.png'
set title "Flux for cold Hydrogen sphere of radius 0.0005 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_1.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_2.png'
set title "Flux for cold Hydrogen sphere of radius 0.001 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_2.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_3.png'
set title "Flux for cold Hydrogen sphere of radius 0.0015 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_3.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_4.png'
set title "Flux for cold Hydrogen sphere of radius 0.002 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_4.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_5.png'
set title "Flux for cold Hydrogen sphere of radius 0.0025 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_5.txt" title "" with errorbars
clear
