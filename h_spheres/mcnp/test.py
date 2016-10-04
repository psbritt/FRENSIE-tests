#! /usr/bin/env python
import pandas
import numpy as np

colnames = ['energy', 'tally', 'sigma']
data = pandas.read_csv('results/1kev_flux_10.txt', names=colnames, sep=' ')
energy = data.energy.tolist()
tally = data.tally.tolist()
sigma = data.sigma.tolist()
print "energy = ", energy[2], "\ttally = ", tally[2], "\tsigma = ", sigma[2]
print "energy = ", energy[198], "\ttally = ", tally[198], "\tsigma = ", sigma[198]

print len(energy)


data2 = pandas.read_csv('../dagmc/results/1kev_flux_12.txt', names=colnames, sep=' ', skiprows=1)
energy2 = data2.energy.tolist()
tally2 = data2.tally.tolist()
sigma2 = data2.sigma.tolist()

print "energy = ", energy2[2], "\ttally = ", tally2[2], "\tsigma = ", sigma2[2]
print "energy = ", energy2[198], "\ttally = ", tally2[198], "\tsigma = ", sigma2[198]

print len(energy2)
ratio = []
ratio_sigma = []
dist = []
ratio_file = open('test.txt', 'w')
ratio_file.write("Energy\tRatio\tSigma\n")
for i in range(0, len(energy2)):
    if tally2[i] == tally[i]:
        ratio.append( 1.0 )
        ratio_sigma.append( np.sqrt(sigma2[i]*sigma2[i] + sigma[i]*sigma[i])*ratio[i])
        dist.append( 1.0 )
        output = str(energy2[i])+" "+str(ratio[i])+" "+str(ratio_sigma[i])+"\n"
        ratio_file.write(output)
    else:
        ratio.append( tally2[i]/tally[i] )
        ratio_sigma.append( np.sqrt(sigma2[i]*sigma2[i] + sigma[i]*sigma[i])*ratio[i])
        dist.append( np.ceil( np.fabs(ratio[i] - 1.0)/ratio_sigma[i]) )
        output = str(energy2[i])+" "+str(ratio[i])+" "+str(ratio_sigma[i])+"\n"
        ratio_file.write(output)
ratio_file.close()

sigma1 = 0
sigma2 = 0
sigma3 = 0
total = float(len(dist))
for i in range(0, len(ratio)):
    print "ratio = ", ratio[i], "\tsigma = ", ratio_sigma[i], "\tdist = ", dist[i]
    if dist[i] == 0:
        sigma1 = sigma1 + 1
        sigma2 = sigma2 + 1
        sigma3 = sigma3 + 1
    elif dist[i] == 1.0:
        sigma1 = sigma1 + 1
        sigma2 = sigma2 + 1
        sigma3 = sigma3 + 1
    elif dist[i] == 2.0:
        sigma2 = sigma2 + 1
        sigma3 = sigma3 + 1
    elif dist[i] == 3.0:
        sigma3 = sigma3 + 1

print "% within 1 sigma = ", sigma1/total, "\n% within 2 sigma = ", sigma2/total, "\n% within 3 sigma = ", sigma3/total

