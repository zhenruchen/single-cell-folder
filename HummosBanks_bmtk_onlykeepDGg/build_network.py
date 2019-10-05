"""
Author: Tyler Banks
Date: 3/9/2019

"""
import cell_positions as p
import synapses

from bmtk.builder.auxi.edge_connectors import distance_connector, connect_random
from bmtk.builder.networks import NetworkBuilder
import math
import numpy as np
import random

def build_hippocampus(output='network', seed=None, experiment=0):
    
    seed_default = 43

    if seed:
        seed_default = seed
    
    random.seed(seed_default)
    np.random.seed(seed_default)

    #initialize the network    
    net = NetworkBuilder('hippocampus')

    
    ###########################################################
    # Build node locations
    ###########################################################
    
    #define cell numbers
    inpTotal = 30 # EC
    excTotal = 63 # CA3 principal
    CA3oTotal = 8
    CA3bTotal  = 8
    DGexcTotal = 384 
    DGbTotal = 32
    DGhTotal = 32

    #get cell positions
    p_EC = p.pos_EC()
    p_CA3e = p.pos_CA3e()
    p_CA3o = p.pos_CA3o()
    p_CA3b = p.pos_CA3b()
    p_DGg = p.pos_DGg()
    p_DGh = p.pos_DGh()
    p_DGb = p.pos_DGb()

    #verify cell numbers match cell position list sizes
    assert len(p_EC) == inpTotal
    assert len(p_CA3e) == excTotal
    assert len(p_CA3o) == CA3oTotal
    assert len(p_CA3b) == CA3bTotal
    assert len(p_DGg) == DGexcTotal
    assert len(p_DGh) == DGhTotal
    assert len(p_DGb) == DGbTotal

    
    ###########################################################
    # Build nodes
    ###########################################################

    #Add noteds to the network
    net.add_nodes(N=inpTotal, pop_name='EC',
                positions=p_EC,
                model_type='biophysical',
                model_template='hoc:IzhiCell_EC',
                morphology='blank.swc'
                )
    net.add_nodes(N=excTotal, pop_name='CA3e',
                positions=p_CA3e,
                model_type='biophysical',
                model_template='hoc:IzhiCell_CA3',
                morphology='blank.swc'
               )
    net.add_nodes(N=CA3oTotal, pop_name='CA3o',
               positions=p_CA3o,
               model_type='biophysical',
               model_template='hoc:IzhiCell_OLM',
                morphology='blank.swc'
                )
    net.add_nodes(N=CA3bTotal, pop_name='CA3b',
                positions=p_CA3b,
                model_type='biophysical',
                model_template='hoc:IzhiCell_BC',
                morphology='blank.swc'
                )
    net.add_nodes(N=DGexcTotal, pop_name='DGg',
                positions=p_DGg,
                model_type='biophysical',
                model_template='hoc:IzhiCell_GC',
                morphology='blank.swc'
                )
    net.add_nodes(N=DGhTotal, pop_name='DGh',
               positions=p_DGh,
                model_type='biophysical',
                model_template='hoc:IzhiCell_OLM',
                morphology='blank.swc'
                )
    net.add_nodes(N=DGbTotal, pop_name='DGb',
                positions=p_DGb,
                model_type='biophysical',
                model_template='hoc:IzhiCell_BC',
                morphology='blank.swc'
                )
    
    ###########################################################
    # Build custom synapses
    ###########################################################
    #See https://github.com/AllenInstitute/bmtk/blob/develop/bmtk/simulator/bionet/default_setters/synapse_models.py

    synapses.load()
    syn = synapses.syn_params_dicts()
    syn_list = []

    ###########################################################
    # Build custom connection rules
    ###########################################################
    #See bmtk.builder.auxi.edge_connectors
    def hipp_dist_connector(source, target, con_pattern, ratio=1, gaussa=0, min_syn=1, max_syn=1):
        """
        :returns: number of synapses per connection

        #Original Hoc Code:

        dx = Locs.o(postArea).x[0][m] - Locs.o(preArea).x[0][b]
        dy = Locs.o(postArea).x[1][m] - Locs.o(preArea).x[1][b]
        
        if ((Locs.o(preArea).nrow + Locs.o(postArea).nrow) > 5) {
            dz = Locs.o(postArea).x[2][m] - Locs.o(preArea).x[2][b]
            dist = sqrt(dx^2 + dy^2 + dz^2) 
            distxy = sqrt(dx^2 + dy^2)
        } else {
            dist = sqrt(dx^2 + dy^2)
            distxy = dist
        }

        // Lamellar. 
            //prob = prob =	 par.x(4) /(1+(1-exp(-abs(dx)^2/3)))	
        // pyr-int feedback loop. Has to be the same loop. Or the same seed? Theoritically I can connect pyr to int, same #the seed and then go through the same seed and loop to connect int to pyr.  
            // it shoudl be based off of interneuron axonal plexus.
        // Random. Turn off the dist component.
            //prob = par.x(4)
        // Mossy  (If 30 of CA3 cells are active, then a recruited gc have a 50% chance of recruiting a new CA3 neuron)
        // within axonal plexus.
        // prob = par.x(4)/dist
                calc dist 
        if (ConPattern == Lamellar) {
            prob =	 par.x(4)/ (exp( ((abs(dx) -0)^2)/ (2 * (3^2)))) //par4 is ratio
        }
        if (ConPattern == Homogenous) {
            prob =	 par.x(4) 			//par4 is ratio 	
        }
        if (ConPattern == IntPyrFeedback || ConPattern == AxonalPlexus) {
            c = par.x(4)
            a = par.x(29) //par29 is GaussA
           
           prob =	 a /(exp( ((abs(distxy) -0)^2)/ (2 * (c^2))))	
        """
        ratio = float(ratio)
        gaussa = float(gaussa)

        Lamellar = "0"
        Homogenous = "1"
        AxonalPlexus = "2"
        IntPyrFeedback = "3"
        
        x_ind,y_ind = 0,1
        dx = target['positions'][x_ind] - source['positions'][x_ind]
        dy = target['positions'][y_ind] - source['positions'][y_ind]
        distxy = math.sqrt(dx**2 + dy**2)
        prob = 1

        if con_pattern == Lamellar:
            prob = ratio/(math.exp(((abs(dx)-0)**2)/(2*(3**2))))
        if con_pattern == Homogenous:
            prob = ratio
        if con_pattern == IntPyrFeedback or con_pattern == AxonalPlexus:
            c = ratio
            a = gaussa
            prob = a /(math.exp(((abs(distxy)-0)**2)/(2*(c**2))))

        if random.random() < prob:
            #Since there will be recurrect connections we need to keep track externally to BMTK
            #BMTK will call build_edges twice if we use net.edges() before net.build()
            #Resulting in double the edge count
            syn_list.append({'source_gid':source['node_id'],'target_gid':target['node_id']})
            return random.randint(min_syn,max_syn)
        else:
            return 0

    ###########################################################
    # Build individual edge properties
    ###########################################################
    #Individual edge properties (See bmtk.docs.tutorials.NetworkBuilder_Intro.ipynb)

    def syn_dist_delay(source, target, base_delay, dist_delay=None):#, min_weight, max_weight):
        """
        Original Code:
        distDelay = 0.1* (0.5*dist + rC.normal(0,1.5)*(1-exp(-dist^2/3)) ) 
        """
        base_delay = float(base_delay)
        if dist_delay:
            dist_delay = float(dist_delay)

        if dist_delay: #An override of sorts
            return base_delay + dist_delay

        x_ind,y_ind,z_ind = 0,1,2
        
        dx = target['positions'][x_ind] - source['positions'][x_ind]
        dy = target['positions'][y_ind] - source['positions'][y_ind]
        dz = target['positions'][z_ind] - source['positions'][z_ind]

        dist = math.sqrt(dx**2 + dy**2 + dz**2)
        distDelay = 0.1* (0.5*dist + np.random.normal(0,1.5,1)[0]*(1-math.exp(-dist**2/3)) ) 
        return float(base_delay) + distDelay

    def syn_dist_delay_section(source, target, base_delay, dist_delay=None, sec_id=0, sec_x=0.9):
        return syn_dist_delay(source, target, base_delay, dist_delay), sec_id, sec_x

    ###########################################################
    # Build connections
    ###########################################################
    #sec_id, sec_x -> https://github.com/tjbanks/bmtk/blob/develop/docs/examples/bio_450cells_exact/build_network.py

    #Connect EC->CA3e Excitatory
    dynamics_file = 'EC2CA3e.exc.json'
    conn = net.add_edges(source={'pop_name': 'EC'}, target={'pop_name': 'CA3e'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    #The following runs into issues... There seems to be a problem calling add_properties twice
    #conn.add_properties(['sec_id','sec_x'],rule=(0, 0.9), dtypes=[np.int32,np.float])
    #conn.add_properties('delay', 
    #            rule=syn_dist_delay,
    #            rule_params={'base_delay':syn[dynamics_file]['delay']},
    #            dtypes=np.float)
    #Fix by calling one function to return all you need
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #import pdb
    #pdb.set_trace()
    #Connect EC->CA3b Excitatory
    dynamics_file = 'EC2CA3b.exc.json'
    conn = net.add_edges(source={'pop_name': 'EC'}, target={'pop_name': 'CA3b'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect DGg->CA3b Excitatory
    dynamics_file = 'DGg2CA3b.exc.json'
    conn = net.add_edges(source={'pop_name': 'DGg'}, target={'pop_name': 'CA3b'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect CA3e->CA3e Excitatory
    dynamics_file = 'CA3e2CA3e.exc.json'
    conn = net.add_edges(source={'pop_name': 'CA3e'}, target={'pop_name': 'CA3e'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect CA3e->CA3b Excitatory
    dynamics_file = 'CA3e2CA3b.exc.json'
    conn = net.add_edges(source={'pop_name': 'CA3e'}, target={'pop_name': 'CA3b'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect CA3o->CA3e Inhibitory
    dynamics_file = 'CA3o2CA3e.inh.json'
    conn = net.add_edges(source={'pop_name': 'CA3o'}, target={'pop_name': 'CA3e'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect CA3b->CA3e Inhibitory
    dynamics_file = 'CA3b2CA3e.inh.json'
    conn = net.add_edges(source={'pop_name': 'CA3b'}, target={'pop_name': 'CA3e'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect CA3b->CA3o Inhibitory
    dynamics_file = 'CA3e2CA3e.inh.json'
    conn = net.add_edges(source={'pop_name': 'CA3b'}, target={'pop_name': 'CA3o'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect EC->DGg Excitatory
    dynamics_file = 'EC2DGg.exc.json'
    conn = net.add_edges(source={'pop_name': 'EC'}, target={'pop_name': 'DGg'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect EC->DGb Excitatory
    dynamics_file = 'EC2DGb.exc.json'
    conn = net.add_edges(source={'pop_name': 'EC'}, target={'pop_name': 'DGb'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect DGg->DGb Excitatory
    dynamics_file = 'DGg2DGb.exc.json'
    conn = net.add_edges(source={'pop_name': 'DGg'}, target={'pop_name': 'DGb'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect DGh->DGg Inhibitory
    dynamics_file = 'DGh2DGg.inh.json'
    conn = net.add_edges(source={'pop_name': 'DGh'}, target={'pop_name': 'DGg'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect DGb->DGg Inhibitory
    dynamics_file = 'DGb2DGg.inh.json'
    conn = net.add_edges(source={'pop_name': 'DGb'}, target={'pop_name': 'DGg'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    #Connect DGb->DGh Inhibitory
    dynamics_file = 'DGb2DGh.inh.json'
    conn = net.add_edges(source={'pop_name': 'DGb'}, target={'pop_name': 'DGh'},
                connection_rule=hipp_dist_connector,
                connection_params={'con_pattern':syn[dynamics_file]['con_pattern'],
                                'ratio':syn[dynamics_file]['ratio'],
                                'gaussa':syn[dynamics_file]['gaussa']},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9},
                dtypes=[np.float, np.int32, np.float])

    ###########################################################
    # Build recurrent connection rules
    ###########################################################
    def hipp_recurrent_connector(source,target,all_edges=[],min_syn=1, max_syn=1):
        """
        General logic:
        1. Given a *potential* source and target
        2. Look through all edges currently made
        3. If any of the current edges contains 
            a. the current source as a previous target of 
            b. the current target as a prevous source
        4. Return number of synapses per this connection, 0 otherwise (no connection)
        """
        for e in all_edges:
            #if source['node_id'] == e.target_gid and target['node_id'] == e.source_gid:
            if source['node_id'] == e['target_gid'] and target['node_id'] == e['source_gid']:
                return random.randint(min_syn,max_syn)

        return 0

    ########################################################### 
    # Build recurrent connections
    ###########################################################

    #Connect CA3e->CA3o Excitatory
    dynamics_file = 'CA3e2CA3o.exc.json'
    conn = net.add_edges(source={'pop_name': 'CA3e'}, target={'pop_name': 'CA3o'},
                connection_rule=hipp_recurrent_connector,
                connection_params={'all_edges':syn_list}, #net.edges()},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'dist_delay':0.1, 'sec_id':0, 'sec_x':0.9}, #Connect.hoc:274 0.1 dist delay
                dtypes=[np.float, np.int32, np.float])

    #Connect DGg->DGh Excitatory
    dynamics_file = 'DGg2DGh.exc.json'
    conn = net.add_edges(source={'pop_name': 'DGg'}, target={'pop_name': 'DGh'},
                connection_rule=hipp_recurrent_connector,
                connection_params={'all_edges':syn_list}, #net.edges()},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'dist_delay':0.1, 'sec_id':0, 'sec_x':0.9}, #Connect.hoc:274 0.1 dist delay
                dtypes=[np.float, np.int32, np.float])
    
    ###########################################################
    # Build strict connection rules
    ###########################################################
    def hipp_MF_connector(source,targets,min_syn=1, max_syn=1):
        """
        Exactly 2 connections from source to target
        Pick a random in the target area
        /docs/tutorial/04_multi_pop.ipynb:384:    
        "To tell the builder to use this schema, we must set iterator='all_to_one'
         in the add_edges method. (By default this is set to 'one_to_one'. You can
         also use 'one_to_all' iterator which will pass in a single source and all
         possible targets)."
        """
        
        total_targets = len(targets)
        syns = np.zeros(total_targets)
        x_ind = 0
        n = 0
        while n < 2:
            target_index = random.randint(0,total_targets-1)
            target = targets[target_index]
            dx = target['positions'][x_ind] - source['positions'][x_ind]

            #prob =	 1/ (exp( ((abs(dx) -0)^2)/ (2 * (2^2)))) // Standard deviation of 2 compared to 3 in pp projections More limited longitudianal spread
            prob = 1/(math.exp(((abs(dx)-0)**2)/(2*(2**2))))
            if random.random() < prob:
                n=n+1
                syns[target_index] = random.randint(min_syn,max_syn)

        return syns

    ########################################################### 
    # Build strict connections
    ###########################################################

    #Connect DGg->CA3e Excitatory (Exactly 2 connections allowed) NOTICE: iterator is 'one_to_all'
    dynamics_file = 'DGg2CA3e.exc.json'
    conn = net.add_edges(source={'pop_name': 'DGg'}, target={'pop_name': 'CA3e'},
                iterator='one_to_all',
                connection_rule=hipp_MF_connector,
                connection_params={},
                syn_weight=1,
                dynamics_params=dynamics_file,
                model_template=syn[dynamics_file]['level_of_detail'],
                distance_range=[0.0, 300.0],
                target_sections=['soma'])
    conn.add_properties(names=['delay', 'sec_id', 'sec_x'],
                rule=syn_dist_delay_section,
                rule_params={'base_delay':syn[dynamics_file]['delay'], 'sec_id':0, 'sec_x':0.9}, #Connect.hoc:274 0.1 dist delay
                dtypes=[np.float, np.int32, np.float])
    
    ###########################################################
    # Create External Networks
    ###########################################################
    targets_used = []

    def hipp_external_connector(source,targets,min_syn=1, max_syn=1):
        """
        For each source external cell, randomly pick one target cell as long as
        it hasn't been targeted previously.
        
        Return: List of synapses to target cells, with only one element set to 1
        """
        total_targets = len(targets)
        syns = np.zeros(total_targets)

        target_found = False
        while not target_found: #Inf loops are bad
            target_index = random.randint(0,total_targets-1)
            if not target_index in targets_used:
                syns[target_index] = 1
                targets_used.append(target_index)
                target_found = True       
        
        return syns

    # We need an external netstim-like input to our nodes
    """
    StimuliTwoPatterns.hoc (Original code explanation)

    Create a pool obj with numbers 0 thru 29 (may be for number of cells in the cell EC)
    Create a Stims list obj
    objref stim, nc[inpTotal * 20], netsyn[inpTotal * 20]

    objref Pat1, Pat2, Pat3 //Picked cells to recieve the pattern
    Pat1 = GenerateVector(length = 10)
        create a picked vector of length 10
        for each in the vector 
            pick a random cell number from the pool
            add that cell to the picked and remove from the pool
        return picked cells
        

    Experiment 0
        tstop = 10000
        StimCount = 16
        StimSpace = tstop / StimCount 		//625
        StimDurRatio = 250 / StimSpace  	//.4
        StimSpaceRatio = StimSpace / tstop 	//0.0625
        
        for j in StimCount (loop StimCount times)
            create s stim object
            that starts j * StimSpace
            
            if j < 6
                applyStim(stim, Pat1, 15) //Apply the stimulus created to the Pat1 set of cells, with a initweight and weightmax of 15 in the pyr2pyr
            else
                applyStim to second set of randomly picked cells
    """

    if experiment == 0:
        exp0net = NetworkBuilder('exp0input')
        exp0net.add_nodes(N=10, model_type='virtual', pat='pat1',exp="0")
        exp0net.add_nodes(N=10, model_type='virtual', pat='pat2',exp="0")

        #See StimuliTwoPatterns.hoc:31 for connection params
        conn = exp0net.add_edges(target=net.nodes(pop_name='EC'),
                        source={'pat':'pat1'},
                        iterator='one_to_all',
                        connection_rule=hipp_external_connector,
                        connection_params={},
                        dynamics_params='NetCon2EC.exc.json',
                        model_template='pyr2pyr',
                        delay=0,
                        syn_weight=1,
                        target_sections=['soma'],  # target soma
                        distance_range=[0.0, 300]
                        )
        conn.add_properties(['sec_id','sec_x'],rule=(0, 0.9), dtypes=[np.int32,np.float])
        
        
        conn = exp0net.add_edges(target=net.nodes(pop_name='EC'),
                        source={'pat':'pat2'},
                        iterator='one_to_all',
                        connection_rule=hipp_external_connector,
                        connection_params={},
                        dynamics_params='NetCon2EC.exc.json',
                        model_template='pyr2pyr',
                        delay=0,
                        syn_weight=1,
                        target_sections=['soma'],  # target soma
                        distance_range=[0.0, 300]
                        )
        conn.add_properties(['sec_id','sec_x'],rule=(0, 0.9), dtypes=[np.int32,np.float])
        
    
    # EXPERIMENT 3 STABILITY Unused unless you provide spiking files to these virtual cells
    
    def target_ind_equals_source_ind(source, targets, offset=0, min_syn=1,max_syn=1):
        # Creates a 1 to 1 mapping between source and destination nodes

        total_targets = len(targets)
        syns = np.zeros(total_targets)
        target_index = source['node_id']
        syns[target_index-offset] = 1   
        
        return syns
        
    if experiment == 3:
        exp3net_CA3 = NetworkBuilder('exp3input_CA3')
        exp3net_CA3.add_nodes(N=excTotal, model_type='virtual', pop_name='poisson_CA3')

        exp3net_DG = NetworkBuilder('exp3input_DG')
        exp3net_DG.add_nodes(N=DGexcTotal, model_type='virtual', pop_name='poisson_DG')

        exp3net_EC = NetworkBuilder('exp3input_EC')
        exp3net_EC.add_nodes(N=inpTotal, model_type='virtual', pop_name='input_EC')

        conn = exp3net_CA3.add_edges(target=net.nodes(pop_name='CA3e'),
                        source={'pop_name':'poisson_CA3'},
                        iterator='one_to_all',
                        connection_rule=target_ind_equals_source_ind,
                        connection_params={},
                        dynamics_params='NetConPoisson.exc.exp3.json',
                        model_template='pyr2pyr',
                        delay=0,
                        syn_weight=1,
                        target_sections=['soma'],
                        distance_range=[0.0,9999])
        conn.add_properties(['sec_id','sec_x'],rule=(0, 0.9), dtypes=[np.int32,np.float])                
        
        #offset = excTotal

        conn = exp3net_DG.add_edges(target=net.nodes(pop_name='DGg'),
                        source={'pop_name':'poisson_DG'},
                        iterator='one_to_all',
                        connection_rule=target_ind_equals_source_ind,
                        connection_params={},#"offset":offset},
                        dynamics_params='NetConPoisson.exc.exp3.json',
                        model_template='pyr2pyr',
                        delay=0,
                        syn_weight=1,
                        target_sections=['soma'],
                        distance_range=[0.0,9999])
        conn.add_properties(['sec_id','sec_x'],rule=(0, 0.9), dtypes=[np.int32,np.float])

        #offset = excTotal + DGexcTotal

        conn = exp3net_EC.add_edges(target=net.nodes(pop_name='EC'),
                        source={'pop_name':'input_EC'},
                        iterator='one_to_all',
                        connection_rule=target_ind_equals_source_ind,
                        connection_params={},#"offset":offset},
                        dynamics_params='NetCon2EC.exc.exp3.json',
                        model_template='pyr2pyr',
                        delay=0,
                        syn_weight=1,
                        target_sections=['soma'],
                        distance_range=[0.0,9999])
        conn.add_properties(['sec_id','sec_x'],rule=(0, 0.9), dtypes=[np.int32,np.float])


    ###########################################################
    # Build networks
    ###########################################################
    net.build()
    net.save_nodes(output_dir=output)    
    net.save_edges(output_dir=output)
    
    if experiment == 0:
        exp0net.build()
        exp0net.save(output_dir=output)
    if experiment == 3:
        exp3net_CA3.build()
        exp3net_CA3.save(output_dir=output)
        exp3net_DG.build()
        exp3net_DG.save(output_dir=output)
        exp3net_EC.build()
        exp3net_EC.save(output_dir=output)
    

if __name__ == "__main__":
    build_hippocampus()