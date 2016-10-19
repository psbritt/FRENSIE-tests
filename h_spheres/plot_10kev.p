reset
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_flux_10.png'
set title "Flux for cold Hydrogen sphere of radius 0.0005 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_flux_10.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_flux_11.png'
set title "Flux for cold Hydrogen sphere of radius 0.001 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_flux_11.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_flux_12.png'
set title "Flux for cold Hydrogen sphere of radius 0.0015 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_flux_12.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_flux_13.png'
set title "Flux for cold Hydrogen sphere of radius 0.002 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_flux_13.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_flux_14.png'
set title "Flux for cold Hydrogen sphere of radius 0.0025 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_flux_14.txt" every ::1 title "" with errorbars
clear

# Plot Current
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_current_10.png'
set title "Current for cold Hydrogen sphere of radius 0.0005 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_current_10.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_current_11.png'
set title "Current for cold Hydrogen sphere of radius 0.001 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_current_11.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_current_12.png'
set title "Current for cold Hydrogen sphere of radius 0.0015 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_current_12.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_current_13.png'
set title "Current for cold Hydrogen sphere of radius 0.002 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_current_13.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_current_14.png'
set title "Current for cold Hydrogen sphere of radius 0.0025 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_current_14.txt" every ::1 title "" with errorbars
clear

# Plot Track Length Flux
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_100.png'
set title "Track-length Flux for cold Hydrogen sphere of radius 0.0005 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Track-length Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_100.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_101.png'
set title "Track-length Flux for cold Hydrogen sphere of radius 0.001 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Track-length Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_101.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_102.png'
set title "Track-length Flux for cold Hydrogen sphere of radius 0.0015 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Track-length Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_102.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_103.png'
set title "Track-length Flux for cold Hydrogen sphere of radius 0.002 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Track-length Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_103.txt" every ::1 title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output '10kev_track_flux_104.png'
set title "Track-length Flux for cold Hydrogen sphere of radius 0.0025 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Track-length Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "10kev_track_flux_104.txt" every ::1 title "" with errorbars
clear

