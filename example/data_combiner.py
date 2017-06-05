#!/usr/bin/python

import sys, getopt
import math as m
import matplotlib.pyplot as plt

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

    # calculate % of c/e values within 1,2,3 sigma
    num_c_e_in_one_sigma = 0
    num_c_e_in_two_sigma = 0
    num_c_e_in_three_sigma = 0
    num_below = 0
    num_above = 0

    start = 0
    for i in range(start,len(c_e_ratio)):
        if c_e_ratio[i] < 1.0:
            num_below = num_below+1
        else:
            num_above = num_above+1

        diff = abs( 1.0 - c_e_ratio[i] )
        #print c_e_ratio[i], diff, 2*c_e_uncert[i]
        if diff <= c_e_uncert[i]:
            num_c_e_in_one_sigma = num_c_e_in_one_sigma + 1
        if diff <= 2*c_e_uncert[i]:
            num_c_e_in_two_sigma = num_c_e_in_two_sigma + 1
        if diff <= 3*c_e_uncert[i]:
            num_c_e_in_three_sigma = num_c_e_in_three_sigma + 1

    print "----------------------------------------------------------------"
    print "% C/E in 1 sigma: "
    print num_c_e_in_one_sigma, len(range(start,len(c_e_ratio))), float(num_c_e_in_one_sigma)/len(range(start,len(c_e_ratio)))
    print "----------------------------------------------------------------"
    print "% C/E in 2 sigma: "
    print num_c_e_in_two_sigma, len(range(start,len(c_e_ratio))), float(num_c_e_in_two_sigma)/len(range(start,len(c_e_ratio)))
    print "----------------------------------------------------------------"
    print "% C/E in 3 sigma: "
    print num_c_e_in_three_sigma, len(range(start,len(c_e_ratio))), float(num_c_e_in_three_sigma)/len(range(start,len(c_e_ratio)))
    print "----------------------------------------------------------------"
    print "% below: ", float(num_below)/len(range(start,len(c_e_ratio)))
    print "% above: ", float(num_above)/len(range(start,len(c_e_ratio)))

    # Plot data
    fig1 = plt.figure(num=1, figsize=(10,5))
    plt.subplot2grid((2,6),(0, 0), colspan=6)
#    plt.xlabel('Energy (MeV)')
    plt.ylabel('Track Length Flux ($\#/cm^2$)')
    plt.title('Comparison of the Track Length Flux in a Sphere of H')
#    plt.xlim(0.85,1.0)
#    #plt.ylim(0.02,0.05)
    plt.plot( energy, mcnp_average_values, label='MCNP')
    plt.plot( energy, facemc_average_values, label='FACEMC-ACE')
    # plot with errorbars
#    plt.errorbar( energy, mcnp_average_values, yerr=mcnp_error, label='MCNP')
#    plt.errorbar( energy, facemc_average_values, yerr=facemc_error, label='FACEMC-ACE')
    plt.legend(loc=2)
    plt.subplot2grid((2,6),(1, 0), colspan=6)
    plt.xlabel('Energy (MeV)')
    plt.ylabel('C/E')
#    plt.ylim(0.9, 1.1)
    plt.plot( energy, c_e_ratio )
    # plot with errorbars
#    plt.errorbar( energy, c_e_ratio, yerr=c_e_uncert)
#    plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show()

if __name__ == "__main__":
    main(sys.argv[1:])
