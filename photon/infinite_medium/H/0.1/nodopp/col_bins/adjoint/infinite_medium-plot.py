#!/usr/bin/python
import sys, os
from optparse import *
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../..'))
from infinite_medium_simulation_plot import plotInfiniteMediumSimulationSpectrum

if __name__ == "__main__":

    # Parse the command line arguments
    parser = OptionParser()
    parser.add_option("--rendezvous_file", type="string", dest="rendezvous_file",
                      help="the rendezvous file to load")
    parser.add_option("--estimator_id", type="int", dest="estimator_id",
                      help="the estimator id to use")
    parser.add_option("--entity_id", type="int", dest="entity_id",
                      help="the entity id to use")
    parser.add_option("--col_bin", type="int", dest="col_bin",
                      help="the collision number bin to use")
    parser.add_option("--mcnp_file", type="string", dest="mcnp_file",
                      help="the mcnp output file to load")
    parser.add_option("--mcnp_file_start", type="int", dest="mcnp_file_start",
                      help="the mcnp output file start line")
    parser.add_option("--mcnp_file_end", type="int", dest="mcnp_file_end",
                      help="the mcnp output file end line")
    parser.add_option("--current", action="store_true", dest="is_a_current",
                      help="the data corresponds to a current")
    parser.add_option("--flux", action="store_false", dest="is_a_current",
                      help="the data corresponds to a flux")
    parser.add_option("--forward", action="store_true", dest="is_forward",
                      help="the data was generated in a forward simulation")
    parser.add_option("--adjoint", action="store_true", dest="is_adjoint",
                      help="the data was generated in an adjoint simulation")
    options,args = parser.parse_args()

    if options.entity_id == 1:
        if options.col_bin == 1:
            #top_ylims = [0.0, 0.007]
            top_ylims = [0.0, 0.009]
            bottom_ylims = [0.8,1.2]
            legend_pos = (0.85,0.72)
            #xlims = [0.07,0.1]
            xlims = [0.0,0.1]
        elif options.col_bin == 2:
            #top_ylims = [0.0, 0.006]
            top_ylims = [0.0, 0.009]
            bottom_ylims = [0.8,1.2]
            legend_pos = (0.95,0.96)
            #xlims = [0.05,0.1]
            xlims = [0.0,0.1]
        elif options.col_bin == 3:
            #top_ylims = [0.0, 0.007]
            top_ylims = [0.0, 0.009]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,0.98)
            #xlims = [0.04,0.1]
            xlims = [0.0,0.1]
        elif options.col_bin == 4:
            #top_ylims = [0.0, 0.008]
            top_ylims = [0.0, 0.009]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,0.98)
            #xlims = [0.04,0.1]
            xlims = [0.0,0.1]
        elif options.col_bin == 5:
            top_ylims = [0.0, 0.009]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 6:
            top_ylims = [0.0, 0.010]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 7:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 8:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 9:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 10:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 11:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 12:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 13:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 14:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 15:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 16:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 17:
            top_ylims = [0.0, 0.015]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 18:
            top_ylims = [0.0, 0.02]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 19:
            top_ylims = [0.0, 0.02]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 20:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 21:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 22:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 23:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 24:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 25:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 26:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 27:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 28:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 29:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 30:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 31:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 32:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 33:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 34:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 35:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 36:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 37:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 38:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 39:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 40:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 41:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 42:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 43:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 44:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 45:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 46:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 47:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 48:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 49:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 50:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 51:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 52:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 53:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 54:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 55:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 56:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 57:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 58:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 59:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 60:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 61:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 62:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 63:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 64:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 65:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 66:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 67:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 68:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 69:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 70:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 71:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 72:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 73:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 74:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 75:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 76:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 77:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 78:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 79:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
        elif options.col_bin == 80:
            top_ylims = [0.0, 0.025]
            bottom_ylims = [0.0,2.0]
            legend_pos = (0.95,1.01)
            xlims = [0.0,0.1]
    elif options.entity_id == 3:
        top_ylims = [0.0, 0.15]
        bottom_ylims = [0.5, 1.5]
        legend_pos = (0.95,0.95)
    elif options.entity_id == 6:
        top_ylims = [0.0, 0.075]
        bottom_ylims = [0.5, 1.5]
        legend_pos = (0.95,0.95)
    elif options.entity_id == 9:
        top_ylims = [0.0, 0.03]
        bottom_ylims = [0.5, 1.5]
        legend_pos = (0.95,0.95)
    elif options.entity_id == 12:
        top_ylims = [0.0, 0.005]
        bottom_ylims = [0.5, 1.5]
        legend_pos = (0.95,0.95)
        
    # Plot the spectrum
    plotInfiniteMediumSimulationSpectrum( options.rendezvous_file,
                                          options.estimator_id,
                                          options.entity_id,
                                          options.mcnp_file,
                                          options.mcnp_file_start,
                                          options.mcnp_file_end,
                                          options.is_a_current,
                                          options.is_forward,
                                          col_bin = options.col_bin,
                                          top_ylims = top_ylims,
                                          bottom_ylims = bottom_ylims,
                                          xlims = xlims,
                                          legend_pos = legend_pos )

    
