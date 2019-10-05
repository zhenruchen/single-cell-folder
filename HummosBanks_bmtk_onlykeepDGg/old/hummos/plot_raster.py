import glob
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from numpy import genfromtxt
import pandas as pd
import h5py
from mpl_toolkits.mplot3d import Axes3D

def plot_raster(files_dir='Outputs', file_regex='008sepsSpikeTime*.txt'):
    """
    Author: Tyler Banks
    Loop through all spike files, create a list of when each cell spikes, plot.
    """
    files = glob.glob(os.path.join(files_dir,file_regex))
    data = None
    
    cell_types = ['EC','CA3e','CA3o','CA3b','DGg','DGh','DGb']
    cell_nums = [30,63,8,8,384,32,32]
    d = [[] for _ in range(sum(cell_nums))]
    
    color_picker=['red','orange','yellow','green','blue','purple','black']
    colors = []
    offset=0
    
    for n, file in enumerate(files):
        data = genfromtxt(file,delimiter=',')
        for i, row in enumerate(data):
            d[int(row[0])+offset].append(row[1])
        offset+=cell_nums[n]-1
        
    for i, n in enumerate(cell_nums):
        for _ in range(n):
            colors.append(color_picker[i])
        
    fig, axs = plt.subplots(1,1)
    axs.eventplot(d,colors=colors)
    axs.set_title(file_regex)
    axs.set_ylabel('Cell Number')
    axs.set_xlabel('Time (ms)')
    axs.legend(cell_types[::-1])
    
    leg = axs.get_legend()
    for i,c in enumerate(color_picker):
        leg.legendHandles[-i-1].set_color(c)
    
    plt.savefig('raster.png')
    
    plt.show()
    
    return

def plot_positions(files_dir='Outputs', file_regex='008sepsLoc*.txt'):
    """
    Author: Tyler Banks
    """
    files = glob.glob(os.path.join(files_dir,file_regex))
    data = None
    
    cell_types = ['EC','CA3e','CA3o','CA3b','DGg','DGh','DGb']
    cell_nums = [30,63,8,8,384,32,32]
    d = [[] for _ in range(sum(cell_nums))]
    
    color_picker=['red','blue','orange','yellow','green','black','purple']
    colors = []
    offset=0
    
    fig = plt.figure()
    ax = Axes3D(fig)
    handles = []

    for n, file in enumerate(files):
        data = genfromtxt(file,delimiter=' ')
        handle = ax.scatter(data[:,0],data[:,1],data[:,2],color=color_picker[n],label=cell_types[n])
        handles.append(handle)
    
    plt.title('Hummos Hippocampus')
    plt.legend(handles=handles)
    plt.show()
    
    return

def plot_spikes(cells_file, cell_models_file, spikes_file, population=None):

    cm_df = pd.read_csv(cell_models_file, sep=' ')
    cm_df.set_index('node_type_id', inplace=True)

    cells_h5 = h5py.File(cells_file, 'r')
    # TODO: Use sonata api
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

    spikes_h5 = h5py.File(spikes_file, 'r')
    spike_gids = np.array(spikes_h5['/spikes/gids'], dtype=np.uint)
    spike_times = np.array(spikes_h5['/spikes/timestamps'], dtype=np.float)
        
    spikes = np.rot90(np.vstack((spike_gids,spike_times))) # Make array [[gid spiketime],[gid2 spiketime2]]

    #spikes = spikes[spikes[:,0].argsort()] # Sort by cell number

    """
    Author: Tyler Banks
    Loop through all spike files, create a list of when each cell spikes, plot.
    """
   
    cell_types = ['EC','CA3e','CA3o','CA3b','DGg','DGh','DGb']
    cell_nums = [30,63,8,8,384,32,32]
    d = [[] for _ in range(sum(cell_nums))]
    
    color_picker=['red','orange','yellow','green','blue','purple','black']
    colors = []
    offset=0
    
    for i, row in enumerate(spikes):
        d[int(row[0])+offset].append(row[1])
            
    for i, n in enumerate(cell_nums):
        for _ in range(n):
            colors.append(color_picker[i])
        
    fig, axs = plt.subplots(1,1)
    axs.eventplot(d,colors=colors)
    axs.set_title('Hipp BMTK')
    axs.set_ylabel('Cell Number')
    axs.set_xlabel('Time (ms)')
    axs.legend(cell_types[::-1])
    
    leg = axs.get_legend()
    for i,c in enumerate(color_picker):
        leg.legendHandles[-i-1].set_color(c)
    
    plt.savefig('raster3_after_pycvode_fixes.png')
    
    plt.show()
    
    return


if __name__ == '__main__':
    if __file__ != sys.argv[-1]:
        plot_raster(sys.argv[-1])
    else:
        #plot_raster()
        plot_spikes(cells_file='../HummosBanks-bmtk/network/hippocampus_nodes.h5', cell_models_file='../HummosBanks-bmtk/network/hippocampus_node_types.csv', spikes_file='../HummosBanks-bmtk/output/spikes.h5')
        #plot_positions()