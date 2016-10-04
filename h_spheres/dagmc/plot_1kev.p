reset
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_flux_12.png'
set title "Flux for cold Hydrogen sphere of radius 0.0005 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_flux_1.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_flux_9.png'
set title "Flux for cold Hydrogen sphere of radius 0.001 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_flux_3.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_flux_6.png'
set title "Flux for cold Hydrogen sphere of radius 0.0015 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_flux_6.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_flux_3.png'
set title "Flux for cold Hydrogen sphere of radius 0.002 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_flux_9.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_flux_1.png'
set title "Flux for cold Hydrogen sphere of radius 0.0025 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Flux" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_flux_12.txt" title "" with errorbars
clear

# Plot Current
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_current_12.png'
set title "Current for cold Hydrogen sphere of radius 0.0005 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_current_1.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_current_9.png'
set title "Current for cold Hydrogen sphere of radius 0.001 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_current_3.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_current_6.png'
set title "Current for cold Hydrogen sphere of radius 0.0015 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_current_6.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_current_3.png'
set title "Current for cold Hydrogen sphere of radius 0.002 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_current_9.txt" title "" with errorbars
clear
set terminal pngcairo nocrop enhanced font 'Verdana,10' size 1000,500 
set output 'results/1kev_current_1.png'
set title "Current for cold Hydrogen sphere of radius 0.0025 cm" 
set xlabel "Energy (MeV)" 
set ylabel "Current" 
#set arrow from 0,1 to 0.01,1 nohead
plot "results/1kev_current_12.txt" title "" with errorbars
clear

