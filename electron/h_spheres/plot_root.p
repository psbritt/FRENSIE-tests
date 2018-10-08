reset
clear

if (!exists("filename")) filename='1kev'
track_flux=filename."_track_flux"

set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500
set xlabel "Energy (MeV)" 
set ylabel "Flux" 

set output track_flux.'_1.png'
set title "Flux for cold Hydrogen sphere of radius 0.0005 cm" 
plot track_flux.'_1.txt' title "" with errorbars
clear

set output track_flux.'_2.png'
set title "Flux for cold Hydrogen sphere of radius 0.001 cm" 
plot track_flux.'_2.txt' title "" with errorbars
clear

set output track_flux.'_3.png'
set title "Flux for cold Hydrogen sphere of radius 0.0015 cm" 
plot track_flux.'_3.txt' title "" with errorbars
clear

set output track_flux.'_4.png'
set title "Flux for cold Hydrogen sphere of radius 0.002 cm" 
plot track_flux.'_4.txt' title "" with errorbars
clear

set output track_flux.'_5.png'
set title "Flux for cold Hydrogen sphere of radius 0.0025 cm" 
plot track_flux.'_5.txt' title "" with errorbars
clear
