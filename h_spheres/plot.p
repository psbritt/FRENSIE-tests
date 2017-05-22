reset
clear

## ---------- Plot Flux ---------- ##
flux="flux"

set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500
set xlabel "Energy (MeV)"
set ylabel "Flux"

set title "Flux for cold Hydrogen sphere of radius 0.0005 cm"
set output flux."_12.png"
plot flux."_12.txt" title "" with errorbars
clear

set title "Flux for cold Hydrogen sphere of radius 0.001 cm"
set output flux."_9.png"
plot flux."_9.txt" title "" with errorbars
clear

set title "Flux for cold Hydrogen sphere of radius 0.0015 cm"
set output flux."_6.png"
plot flux."_6.txt" title "" with errorbars
clear

set title "Flux for cold Hydrogen sphere of radius 0.002 cm"
set output flux."_3.png"
plot flux."_3.txt" title "" with errorbars
clear

set title "Flux for cold Hydrogen sphere of radius 0.0025 cm"
set output flux."_1.png"
plot flux."_1.txt" title "" with errorbars
clear

## ---------- Plot Current ---------- ##
current="current"
set ylabel "Current"

set title "Current for cold Hydrogen sphere of radius 0.0005 cm"
set output current."_12.png"
plot current."_12.txt" title "" with errorbars
clear

set title "Current for cold Hydrogen sphere of radius 0.001 cm"
set output current."_9.png"
plot current."_9.txt" title "" with errorbars
clear

set title "Current for cold Hydrogen sphere of radius 0.0015 cm"
set output current."_6.png"
plot current."_6.txt" title "" with errorbars
clear

set title "Current for cold Hydrogen sphere of radius 0.002 cm"
set output current."_3.png"
plot current."_3.txt" title "" with errorbars
clear

set title "Current for cold Hydrogen sphere of radius 0.0025 cm"
set output current."_1.png"
plot current."_1.txt" title "" with errorbars
clear

## ---------- Plot Track Length Flux ---------- ##
track_flux="track_flux"
set ylabel "Flux" 

set output track_flux.'_13.png'
set title "Flux for cold Hydrogen sphere of radius 0.0005 cm" 
plot track_flux."_13.txt" title "" with errorbars
clear

set output track_flux.'_12.png'
set title "Flux for cold Hydrogen sphere of radius 0.001 cm" 
plot track_flux."_12.txt" title "" with errorbars
clear

set output track_flux.'_9.png'
set title "Flux for cold Hydrogen sphere of radius 0.0015 cm" 
plot track_flux."_9.txt" title "" with errorbars
clear

set output track_flux.'_6.png'
set title "Flux for cold Hydrogen sphere of radius 0.002 cm" 
plot track_flux."_6.txt" title "" with errorbars
clear

set output track_flux.'_3.png'
set title "Flux for cold Hydrogen sphere of radius 0.0025 cm" 
plot track_flux."_3.txt" title "" with errorbars
clear

