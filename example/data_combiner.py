#!/usr/bin/python

import sys, getopt
import math as m
import matplotlib.pyplot as plt
from colorama import Fore, init
init(autoreset=True)

def main(argv):
    mcnpinputfile = ''
    facemcinputfile = ''
    outputname = ''
    try:
        opts, args = getopt.getopt(argv,"hm:f:o:",["mfile=","ffile=","ofile="])
    except getopt.GetoptError:
        print 'data_combiner.py -m <mcnpinputfile> -f <facemcinputfile -o <outputname>'
        sys.exit(1)
    for opt, arg in opts:
        if opt == '-h':
            print 'data_combiner.py -m <mcnpinputfile> -f <facemcinputfile -o <outputname>'
            sys.exit(1)
        elif opt in ("-m", "--mfile"):
            mcnpinputfile = arg
        elif opt in ("-f", "--ffile"):
            facemcinputfile = arg
        elif opt in ("-o", "--ofile"):
            outputname = arg

    outputfile = outputname+'.txt'
    output_c_e = outputname+'_c_e.txt'
    outputgraph = outputname+'.png'
    # open the estimator file
    f = open(facemcinputfile, 'r')

    words = []
    facemc_energy = []
    facemc_value = []
    facemc_error = []
    for line in f:
        words = line.split()
        if words[0] != "#":
            facemc_energy.append( float(words[0]) )
            facemc_value.append( float(words[1]) )
            facemc_error.append( float(words[2]) )

    facemc_error.pop(0)

    f.close()

    # open the mcnp file
    f = open(mcnpinputfile, 'r')

    words = []
    mcnp_energy = []
    mcnp_value = []
    mcnp_error = []
    for line in f:
        words = line.split()
        if words[0] != '#':
            mcnp_energy.append( float(words[0]) )
            mcnp_value.append( float(words[1]) )
            mcnp_error.append( float(words[2]) )

    mcnp_error.pop(0)

    f.close()

    # Calculate the average value in the bin
    energy = []
    facemc_average_values = []
    mcnp_average_values = []
    for i in range(1,len(facemc_energy)):
        energy.append( (facemc_energy[i-1] + facemc_energy[i])/2 )
        facemc_average_values.append( facemc_value[i]/(facemc_energy[i]-facemc_energy[i-1]) )
        mcnp_average_values.append( mcnp_value[i]/(mcnp_energy[i]-mcnp_energy[i-1]) )

    # Calculate the propagated uncertainty
    prop_uncert = []

    for i in range(0,len(energy)):
        if mcnp_average_values[i] > 0:
            prop_uncert.append( m.sqrt( ((1.0/mcnp_average_values[i])**2)*(facemc_average_values[i]*facemc_error[i])**2 + ((facemc_average_values[i]/mcnp_average_values[i]**2)**2)*(mcnp_average_values[i]*mcnp_error[i])**2 ) )
        else:
            prop_uncert.append( 0.0 )

    # Create the output file
    f = open(outputfile, 'w')
    f.write( "#MCNP     FACEMC\n" )
    f.write( "#Energy    Values    Error\n" )

    for i in range(0,len(energy)):
        line = ' '
        line = line + str(energy[i])
        line = line + ' '
        line = line + str(mcnp_average_values[i])
        line = line + ' '
        line = line + str(mcnp_error[i])
        line = line + ' '
        line = line + str(facemc_average_values[i])
        line = line + ' '
        line = line + str(facemc_error[i])
        line = line + ' '
        line = line + str(prop_uncert[i])
        line = line + '\n'

        f.write( line )

    # Calculate c/e values
    c_e_ratio = [None]*len(energy)
    c_e_uncert = [None]*len(energy)
    print "----------------------------------------------------------------"
    print "Energy,\t  Facemc,\tMCNP,\t   C/E Ratio\tC/E Uncertainty"
    print "----------------------------------------------------------------"
    for i in range(0,len(energy)):
        if mcnp_average_values[i] > 0 and facemc_average_values[i] > 0:
            c_e_ratio[i] = ( facemc_average_values[i]/mcnp_average_values[i] )
            c_e_uncert[i] = ( prop_uncert[i] )
        elif mcnp_average_values[i] == facemc_average_values[i]:
            c_e_ratio[i] = 1.0
            c_e_uncert[i] = ( prop_uncert[i] )
        else:
            c_e_ratio[i] = 0.0
            c_e_uncert[i] = ( prop_uncert[i] )
        print energy[i], "\t", facemc_average_values[i], "\t", mcnp_average_values[i], c_e_ratio[i], "\t", c_e_uncert[i]

    # calculate % of c/e values within 1,2,3 sigma
    num_c_e_in_one_sigma = 0
    num_c_e_in_two_sigma = 0
    num_c_e_in_three_sigma = 0
    num_below = 0
    num_above = 0

    start = 0
    stop = len(c_e_ratio)
    num_zeros = 0
    print "----------------------------------------------------------------"
    print "Energy,\t Difference in units Sigma,\t Sigma"
    print "----------------------------------------------------------------"
    for i in range(start,stop):
        if c_e_ratio[i] < 1.0:
            num_below = num_below+1
        else:
            num_above = num_above+1

        diff = abs( 1.0 - c_e_ratio[i] )
        if ( c_e_uncert[i] > 0.0 ):
          string = str(energy[i])+ "\t"+ str(diff/c_e_uncert[i]) + "\t" + str(c_e_uncert[i])
        elif ( diff == 0.0 ):
          string = str(energy[i])+ "\t0.0\t" + str(c_e_uncert[i])
          num_zeros = num_zeros + 1
          continue
        else:
          string = str(energy[i])+ "\tinf\t" + str(c_e_uncert[i])
        #print c_e_ratio[i], diff, 2*c_e_uncert[i]
        if diff <= c_e_uncert[i]:
            num_c_e_in_one_sigma = num_c_e_in_one_sigma + 1
            print(Fore.GREEN + str(string))
        if diff <= 2*c_e_uncert[i]:
            num_c_e_in_two_sigma = num_c_e_in_two_sigma + 1
            if diff > c_e_uncert[i]:
                print(Fore.BLUE + str(string))
        if diff <= 3*c_e_uncert[i]:
            num_c_e_in_three_sigma = num_c_e_in_three_sigma + 1
            if diff > 2*c_e_uncert[i]:
                print(Fore.YELLOW + str(string))
        else:
            print(Fore.RED + str(string))

    length = len(range(start,len(c_e_ratio))) - num_zeros
    print "----------------------------------------------------------------"
    print(Fore.GREEN + "% C/E in 1 sigma: ")
    string = str(num_c_e_in_one_sigma) + " " + str(length) + " " + str(float(num_c_e_in_one_sigma)/length)
    print(Fore.GREEN + str(string))
    print "----------------------------------------------------------------"
    print(Fore.BLUE + "% C/E in 2 sigma: ")
    string = str(num_c_e_in_two_sigma) + " " + str(length) + " " + str(float(num_c_e_in_two_sigma)/length)
    print(Fore.BLUE + str(string))
    print "----------------------------------------------------------------"
    print(Fore.YELLOW + "% C/E in 3 sigma: ")
    string = str(num_c_e_in_three_sigma) + " " + str(length) + " " + str(float(num_c_e_in_three_sigma)/length)
    print(Fore.YELLOW + str(string))
    print "----------------------------------------------------------------"
    print "% below: ", float(num_below)/length
    print "% above: ", float(num_above)/length

    # Create the output file for C/E data
    f = open(output_c_e, 'w')
    f.write( "#FACEMC/MCNP\n" )
    f.write( "#Energy    Values    Error\n" )

    for i in range(0,len(energy)):
        line = ' '
        line = line + str(energy[i])
        line = line + ' '
        line = line + str(c_e_ratio[i])
        line = line + ' '
        line = line + str(c_e_uncert[i])
        line = line + '\n'

        f.write( line )

    # Plot data
    fig1 = plt.figure(num=1, figsize=(10,5))
    ax =plt.subplot2grid((2,6),(0, 0), colspan=6)

    # plt.ylabel('Surface Current ($\#$)')
    # plt.ylabel('Surface Flux ($\#/cm^2$)')
    plt.ylabel('Track Length Flux ($\#/cm^2$)')
    # plt.title('Comparison of the Surface Current in a Sphere of H')
    # plt.title('Comparison of the Surface Flux in a Sphere of H')
    plt.title('Comparison of the Track Length Flux in a Sphere of H')
    # plt.ylim(2e4, 2e6)
    # ax.set_yscale('log')

    plt.xlim(0.0, energy[len(energy)-1])

    # plot with errorbars
    plt.errorbar( energy, mcnp_average_values, yerr=mcnp_error, label='MCNP 6.2')
    plt.errorbar( energy, facemc_average_values, yerr=facemc_error, label='ACE-EPR14')
    plt.legend(loc=2)
    plt.subplot2grid((2,6),(1, 0), colspan=6)
    plt.xlabel('Energy (MeV)')
    plt.ylabel('C/E')
    plt.xlim(1e-5, energy[len(energy)-1])

    # plot with errorbars
    plt.errorbar( energy, c_e_ratio, yerr=c_e_uncert, color='r')

    fig1.savefig(outputgraph, bbox_inches='tight', dpi=300)
    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
