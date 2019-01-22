import numpy
import time
import math as m
import matplotlib.pyplot as plt
import PyFrensie.Utility as Utility
import PyFrensie.MonteCarlo.Photon as Photon

def sampleAngle( native_data,
                 model_type,
                 sampling_type,
                 num_samples,
                 incoming_energy,
                 max_energy,
                 evaluate_pdf = False ):

    # Create the distribution
    dist = Photon.IncoherentAdjointPhotonScatteringDistributionNativeFactory.createDistribution(
                                                             native_data,
                                                             model_type,
                                                             sampling_type,
                                                             max_energy )

    sampled_energies = [0]*num_samples
    sampled_mus = [0]*num_samples
    trials = 0

    start = time.time()
    for i in range(0,num_samples):
        sampled_energies[i],sampled_mus[i],trials = dist.sampleAndRecordTrials( incoming_energy, trials )
    end = time.time()

    return_values = [num_samples/float(trials), num_samples/(end-start)]

    if evaluate_pdf:
        pdf = [0]*1001
        mu = [0]*1001
        mu_min = Photon.calculateMinScatteringAngleCosine( incoming_energy, max_energy )
        mu_step = (1.0 - mu_min)/(len(pdf)-1)

        for i in range(0,len(pdf)):
            mu[i] = mu_min + mu_step*i
            pdf[i] = dist.evaluatePDF( incoming_energy, mu[i] )

        return_values.append( sampled_energies )
        return_values.append( sampled_mus )
        return_values.append( mu )
        return_values.append( pdf )

    return return_values

def sampleAngleAndPlot( native_data,
                        model_type,
                        sampling_type,
                        num_samples,
                        incoming_energy,
                        max_energy ):

    efficiency,samples_per_sec,sampled_energies,sampled_mus,mu,pdf = \
        sampleAngle( native_data,
                     model_type,
                     sampling_type,
                     num_samples,
                     incoming_energy,
                     max_energy,
                     True )

    print "samples per second:", samples_per_sec
    print "efficiency:", efficiency
        
    plt.plot( mu, pdf )
    plt.hist( sampled_mus, bins=150, normed=True )
    plt.show()
