import synapses

import glob, os, re, sys
from bmtk.simulator import bionet
from bmtk.simulator.bionet.default_setters.cell_models import loadHOC
from bmtk.utils.io.spike_trains import SpikeTrainWriter
from bmtools import util

import h5py
import numpy as np
from numpy import genfromtxt
import pandas as pd

def generate_exp0_input(input_dir='input',output_filename='exp0_input.csv', tstop=10000,
                        stim_interval=80, num_p1=10, num_p2=10):
    #https://github.com/tjbanks/bmtk/blob/develop/bmtk/utils/io/spike_trains.py
    stim_count = 16
    spike_writer = SpikeTrainWriter(tmp_dir=input_dir)
    
    stim_space = tstop / stim_count 	#//625
    stim_dur_ratio = 250 / stim_space  	#//.4
    stim_space_ratio = stim_space / tstop 	#//0.0625
    
    stim_interval = 80
    # We want to apply the first set of stimulus to all cells in num_p1 and
    # apply the second set of stimulus to all cells in num_p2

    #for each j in stim_count
        #apply stim to each cell in num_p (if j<6 apply to cells 0-9, else cells 10-19)

    stim_number = (stim_space * stim_dur_ratio) / stim_interval
    stims = {}
    def apply_stim(stim_start, cell_ids):
        for cell in cell_ids:
            for spike_time in range(int(stim_start),int(stim_start+(stim_number*stim_interval)),int(stim_interval)):
                if not stims.get(cell):
                    stims[cell] = []
                stims[cell].append(spike_time)
                #spike_writer.add_spike(spike_time,cell)
        return

    for j in range(stim_count):
        stim_start = j * (stim_space)
        if j < 5:
            apply_stim(stim_start,[j for j in range(0,num_p1)])
        else:
            apply_stim(stim_start,[j for j in range(num_p1,num_p1+num_p2)])
    
    #spike_writer.to_csv(os.path.join(input_dir,output_filename),sort_order='gid')
    #Spikes must be in the format
    #gid spike-times
    #0 0,2,3,45,3
    #...
    #n 0
    #With all cell accounted for.

    with open(os.path.join(input_dir,output_filename),'w') as file:
        file.write('gid spike-times\n')
        for key, value in stims.items():
            file.write(str(key)+' '+','.join(str(x) for x in value)+'\n') 
    
    
    
def print_edge_list(config_file):
    bionet.pyfunction_cache.add_cell_model(loadHOC, directive='hoc', model_type='biophysical')
    synapses.load()
    conf = bionet.Config.from_json(config_file, validate=True)  
    conf.build_env()
    graph = bionet.BioNetwork.from_config(conf)
    sim = bionet.BioSimulator.from_config(conf, network=graph)

    for e in sim.net._edge_populations[0].get_edges():
        print(e.source_node_id,'-->',e.target_node_id)

"""
Want to be able to generate plots of connectivity between cell types
Heatmaps with annotation is a good way to express this information
https://matplotlib.org/gallery/images_contours_and_fields/image_annotated_heatmap.html

Wants:
Number of synapses from/to cell types
Percent connectivity
Average number of synapses per connection
Average divergence (each presynaptic cell typically connects to an average of x post synaptic cells)
Average convergence (each post synaptic cell typically recieves )

Split this into 3 methods
    1. Get data returns connection list, list of region names, list of cell numbers per region
    2. Perform operation, returns matrix with values
    3. Plot matrix heatmap with annotated values
"""

def load_nodes(network_dir="network", show_virtual=False):
    """
        Glob all files for *_nodes.h5
        Glob all files for *_edges.h5

    """
    nodes_regex = "_nodes.h5"
    node_types_regex = "_node_types.csv"

    nodes_h5_fpaths = glob.glob(os.path.join(network_dir,'*'+nodes_regex))
    node_types_fpaths = glob.glob(os.path.join(network_dir,'*'+node_types_regex))

    regions = [re.findall('^[^_]+', os.path.basename(n))[0] for n in nodes_h5_fpaths]
    region_dict = {}

    #Need to get all cell groups for each region
    def get_node_table(cell_models_file, cells_file, population=None):
        cm_df = pd.read_csv(cell_models_file, sep=' ')
        cm_df.set_index('node_type_id', inplace=True)

        cells_h5 = h5py.File(cells_file, 'r')
        if population is None:
            if len(cells_h5['/nodes']) > 1:
                raise Exception('Multiple populations in nodes file. Please specify one to plot using population param')
            else:
                population = list(cells_h5['/nodes'])[0]

        nodes_grp = cells_h5['/nodes'][population]
        c_df = pd.DataFrame({'node_id': nodes_grp['node_id'], 'node_type_id': nodes_grp['node_type_id']})

        c_df.set_index('node_id', inplace=True)
        nodes_df = pd.merge(left=c_df,
                            right=cm_df,
                            how='left',
                            left_on='node_type_id',
                            right_index=True)  # use 'model_id' key to merge, for right table the "model_id" is an index
        return nodes_df
    
    for region, cell_models_file, cells_file in zip(regions, node_types_fpaths, nodes_h5_fpaths):
        region_dict[region] = get_node_table(cell_models_file,cells_file)

    #cell_num = 2
    #print(region_dict["hippocampus"].iloc[cell_num]["node_type_id"])
    #print(list(set(region_dict["hippocampus"]["node_type_id"]))) #Unique

    return region_dict

def load_connections(network_dir='network'):
    """
    Returns: A dictionary of connections with filenames (minus _edges.h5) as keys
    """
    
    edges_regex = "_edges.h5"
    edge_types_regex = "_edge_types.csv"

    edges_h5_fpaths = glob.glob(os.path.join(network_dir,'*'+edges_regex))
    edge_types_fpaths = glob.glob(os.path.join(network_dir,'*'+edge_types_regex))

    connections = [re.findall('^[A-Za-z0-9]+_[A-Za-z0-9][^_]+', os.path.basename(n))[0] for n in edges_h5_fpaths]
    connections_dict = {}

    def get_connection_table(connection_models_file, connections_file,population=None):
        cm_df = pd.read_csv(connection_models_file, sep=' ')
        cm_df.set_index('edge_type_id', inplace=True)

        connections_h5 = h5py.File(connections_file, 'r')
        # TODO: Use sonata api
        if population is None:
            if len(connections_h5['/edges']) > 1:
                raise Exception('Multiple populations in edges file. Please specify one to plot using population param')
            else:
                population = list(connections_h5['/edges'])[0]

        conn_grp = connections_h5['/edges'][population]
        c_df = pd.DataFrame({'edge_type_id': conn_grp['edge_type_id'], 'source_node_id': conn_grp['source_node_id'],
                             'target_node_id': conn_grp['target_node_id']})

        c_df.set_index('edge_type_id', inplace=True)

        nodes_df = pd.merge(left=c_df,
                            right=cm_df,
                            how='left',
                            left_index=True,
                            right_index=True)  # use 'model_id' key to merge, for right table the "model_id" is an index
        return nodes_df
    
    for connection, conn_models_file, conns_file in zip(connections, edge_types_fpaths, edges_h5_fpaths):
        connections_dict[connection] = get_connection_table(conn_models_file,conns_file)

    return connections_dict


def connection_totals(nodes=None,edges=None,populations=[]):
    if not nodes:
        nodes = load_nodes()
    if not edges:
        edges = load_connections()

    total_cell_types = len(list(set(nodes[populations[0]]["node_type_id"])))
    nodes_hip = pd.DataFrame(nodes[populations[0]])
    pop_names = nodes_hip.pop_name.unique()

    e_matrix = np.zeros((total_cell_types,total_cell_types))

    for i, key in enumerate(list(edges)):
        if i==0:#TODO TAKE OUT FROM TESTING
            continue
        
        for j, row in edges[key].iterrows():
            source = row["source_node_id"]
            target = row["target_node_id"]
            source_node_type = nodes[populations[0]].iloc[source]["node_type_id"]
            target_node_type = nodes[populations[0]].iloc[target]["node_type_id"]

            source_index = int(source_node_type - 100)
            target_index = int(target_node_type - 100)

            e_matrix[source_index,target_index]+=1
            
    return e_matrix, pop_names

def percent_connectivity(nodes=None, edges=None, conn_totals=None, pop_names=None,populations=[]):
    if nodes == None:
        nodes = load_nodes()
    if edges == None:
        edges = load_connections()
    if conn_totals == None:
        conn_totals,pop_names=connection_totals(nodes=nodes,edges=edges,populations=populations)

    #total_cell_types = len(list(set(nodes[populations[0]]["node_type_id"])))
    vc = nodes[populations[0]].apply(pd.Series.value_counts)
    vc = vc["node_type_id"].dropna().sort_index()
    vc = list(vc)

    max_connect = np.ones((len(vc),len(vc)),dtype=np.float)

    for a, i in enumerate(vc):
        for b, j in enumerate(vc):
            max_connect[a,b] = i*j
    ret = conn_totals/max_connect
    ret = ret*100
    ret = np.around(ret, decimals=1)

    return ret, pop_names

def original_connection_totals(synapses_file):
    data = genfromtxt(synapses_file,delimiter=' ')
    cell_types = ['EC','CA3e','CA3o','CA3b','DGg','DGh','DGb']
    total_cell_types = len(cell_types)
    cell_nums = [30,63,8,8,384,32,32]
    cell_start = [sum(cell_nums[:i]) for i,v in enumerate(cell_nums)]

    e_matrix = np.zeros((total_cell_types,total_cell_types))
    for i, row in enumerate(data):
        e_matrix[int(row[1]),int(row[3])]+=1

    return e_matrix, cell_types

def original_percent_connectivity(synapses_file):
    conn_totals, cell_types = original_connection_totals(synapses_file)
    
    cell_nums = [30,63,8,8,384,32,32]
    total_cell_types = len(cell_nums)

    max_connect = np.ones((total_cell_types,total_cell_types),dtype=np.float)

    for a, i in enumerate(cell_nums):
        for b, j in enumerate(cell_nums):
            max_connect[a,b] = i*j
    ret = conn_totals/max_connect
    ret = ret*100
    ret = np.around(ret, decimals=1)

    return ret, cell_types

def original_connection_divergence_average(synapses_file,convergence=False):
    conn_totals, cell_types = original_connection_totals(synapses_file)
    
    cell_nums = [30,63,8,8,384,32,32]
    total_cell_types = len(cell_nums)

    e_matrix = np.ones((total_cell_types,total_cell_types),dtype=np.float)

    for a, i in enumerate(cell_nums):
        for b, j in enumerate(cell_nums):
            c = b if convergence else a
            e_matrix[a,b] = conn_totals[a,b]/cell_nums[c]

    ret = np.around(e_matrix, decimals=1)

    return ret, cell_types

def connection_average_synapses():
    return

def connection_divergence_average(nodes=None, edges=None,populations=[],convergence=False):
    """
    For each cell in source count # of connections in target and average
    """
    if nodes == None:
        nodes = load_nodes()
    if edges == None:
        edges = load_connections()

    nodes_hip = pd.DataFrame(nodes[populations[0]])
    pop_names = nodes_hip.pop_name.unique()

    nodes = nodes[list(nodes)[1]]
    edges = edges[list(edges)[1]]

    src_df = pd.DataFrame({'edge_node_id': nodes.index,'source_node_pop_name':nodes['pop_name'],'source_node_type_id':nodes['node_type_id']})
    tgt_df = pd.DataFrame({'edge_node_id': nodes.index,'target_node_pop_name':nodes['pop_name'],'target_node_type_id':nodes['node_type_id']})
    
    src_df.set_index('edge_node_id', inplace=True)
    tgt_df.set_index('edge_node_id', inplace=True)
    
    edges_df = pd.merge(left=edges,
                            right=src_df,
                            how='left',
                            left_on='source_node_id',
                            right_index=True)
    
    edges_df = pd.merge(left=edges_df,
                            right=tgt_df,
                            how='left',
                            left_on='target_node_id',
                            right_index=True)
    
    edges_df_trim = edges_df.drop(edges_df.columns.difference(['source_node_type_id','target_node_type_id','source_node_pop_name','target_node_pop_name']), 1, inplace=False)

    vc = nodes.apply(pd.Series.value_counts)
    vc = vc["node_type_id"].dropna().sort_index()
    vc = list(vc)

    """
    For each source type
        For each target type
            temp = df[(df.src == source) & (df.tgt < target)]
            #edge_totals[src,tgt] = temp.sum
    """
    src_list_node_types = list(set(edges_df_trim["source_node_type_id"]))
    tgt_list_node_types = list(set(edges_df_trim["target_node_type_id"]))
    node_types = list(set(src_list_node_types+tgt_list_node_types))

    e_matrix = np.zeros((len(node_types),len(node_types)))

    for a, i in enumerate(node_types):
        for b, j in enumerate(node_types):
            num_conns = edges_df_trim[(edges_df_trim.source_node_type_id == i) & (edges_df_trim.target_node_type_id==j)].count()
            c = b if convergence else a #Show convergence if set. By dividing by targe totals instead of source

            e_matrix[a,b] = num_conns.source_node_type_id/vc[c]

    ret = np.around(e_matrix, decimals=1)

    return ret, pop_names

def plot_connection_info(data, labels, title):
    import numpy as np
    import matplotlib
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots()
    im = ax.imshow(data)

    # We want to show all ticks...
    ax.set_xticks(np.arange(len(labels)))
    ax.set_yticks(np.arange(len(labels)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)


    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
            rotation_mode="anchor")

    # Loop over data dimensions and create text annotations.
    for i in range(len(labels)):
        for j in range(len(labels)):
            text = ax.text(j, i, data[i, j],
                        ha="center", va="center", color="w")
    ax.set_ylabel('Source')
    ax.set_xlabel('Target')
    ax.set_title(title)
    fig.tight_layout()
    plt.show()
    return


if __name__ == '__main__':
    if __file__ != sys.argv[-1]:
        pass
        #run(sys.argv[-1])
    else:
        nodes = load_nodes()
        edges = load_connections()

        ### Banks BMTK Model ###
        #data,labels = connection_totals(nodes=nodes, edges=edges, populations=["hippocampus"])
        #plot_connection_info(data, labels, 'BMTK Model Connection Totals')

        #data, labels = percent_connectivity(nodes=nodes, edges=edges, populations=["hippocampus"])
        #plot_connection_info(data, labels, 'BMTK Model Connection Percentages')
        
        #data, labels = connection_divergence_average(nodes=nodes, edges=edges, populations=["hippocampus"],convergence=False)
        #plot_connection_info(data, labels, 'BMTK Model Average Divergence')

        #data, labels = connection_divergence_average(nodes=nodes, edges=edges, populations=["hippocampus"],convergence=True)
        #plot_connection_info(data, labels, 'BMTK Model Average Convergence')


        ### Hummos model ###
        #data,labels = original_connection_totals('../HummosEtAl2014/Outputs/008sepsConnections.txt')
        #plot_connection_info(data, labels, 'Hummos Model Connection Totals')

        #data,labels = original_percent_connectivity('../HummosEtAl2014/Outputs/008sepsConnections.txt')
        #plot_connection_info(data, labels, 'Hummos Model Connection Percentage')

        data, labels = original_connection_divergence_average('../HummosEtAl2014/Outputs/008sepsConnections.txt',convergence=False)
        plot_connection_info(data, labels, 'Hummos Model Average Divergence')

        data, labels = original_connection_divergence_average('../HummosEtAl2014/Outputs/008sepsConnections.txt',convergence=True)
        plot_connection_info(data, labels, 'Hummos Model Average Convergence')

        #generate_exp0_input()