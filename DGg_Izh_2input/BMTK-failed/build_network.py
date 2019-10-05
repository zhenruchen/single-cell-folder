from bmtk.builder.auxi.edge_connectors import distance_connector, connect_random
from bmtk.builder.networks import NetworkBuilder
import math
import numpy as np
import random

import cell_positions as p
p_DGg = p.pos_DGg()

print(p_DGg)
net = NetworkBuilder('cortex')
#net.add_nodes(cell_name='Cell_A',
#              potental='exc',
#              model_type='biophysical',
#              model_template='hoc:CA3PyramidalCell',
#              morphology=None
#              )

net.add_nodes(  N=1, 
		pop_name='DGg',
                #positions=p_DGg,
                model_type='biophysical',
                model_template='hoc:DGCell',
                morphology='blank.swc'
                )

net.build()
net.save_nodes(output_dir='network')

thalamus = NetworkBuilder('mthalamus')
thalamus.add_nodes(N=2,
                   pop_name='tON',
                   potential='exc',
                   level_of_detail='filter')


thalamus.add_edges(source={'pop_name': 'tON'}, target=net.nodes(),
                   connection_rule=5,
                   syn_weight=0.001,
                   delay=2.0,
                   weight_function='wmax',
                   target_sections=['basal', 'apical'],
                   distance_range=[0.0, 150.0],
                   dynamics_params='AMPA_ExcToExc.json',
                   model_template='exp2syn')



thalamus.build()
thalamus.save(output_dir='network')

for node in net.nodes():
    print(node)

                #$BASE_DIR
from bmtk.utils.sim_setup import build_env_bionet

build_env_bionet(base_dir='.',      # Where to save the scripts and config files 
                 components_dir='components',
                 network_dir='network',    # Location of directory containing network files
                 tstop=2000.0, dt=0.1,     # Run a simulation for 2000 ms at 0.1 ms intervals
                 report_vars=['v'], # Tells simulator we want to record membrane potential and calcium traces

                 compile_mechanisms=True   # Will try to compile NEURON mechanisms
                )
                
