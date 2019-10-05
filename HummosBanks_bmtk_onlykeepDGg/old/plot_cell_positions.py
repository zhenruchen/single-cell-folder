from bmtk.analyzer import nodes_table
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import pdb
from mpl_toolkits.mplot3d import Axes3D
import h5py

#A = nodes_table(nodes_file='network/hippocampus_nodes.h5', population='hippocampus')

#dset = np.array(A['positions'].values)
#pos_df = pd.DataFrame(list(dset))
#pos_ds = pos_df.values

f = h5py.File('network/hippocampus_nodes.h5')
pos = (f['nodes']['hippocampus']['0']['positions'])
post = [list(i) for i in list(pos)]
pos_ds = np.array(post)

#inpTotal = 30 # EC
#excTotal = 63 # CA3 principal
#CA3oTotal = 8
#CA3bTotal  = 8
#DGexcTotal = 384 
#DGbTotal = 32
#DGhTotal = 32

fig = plt.figure()
ax = Axes3D(fig)
#ax.scatter(pos_ds[0:599,0],pos_ds[0:599,1],pos_ds[0:599,2],color='red')
#ax.scatter(pos_ds[600:699,0],pos_ds[600:699,1],pos_ds[600:699,2],color='blue')
ec = ax.scatter(pos_ds[0:29,0],pos_ds[0:29,1],pos_ds[0:29,2],color='red',label='EC')

ca3e = ax.scatter(pos_ds[30:92,0],pos_ds[30:92,1],pos_ds[30:92,2],color='blue',label='CA3e')
ca3o = ax.scatter(pos_ds[93:100,0],pos_ds[93:100,1],pos_ds[93:100,2],color='orange',label='CA3o')
ca3b = ax.scatter(pos_ds[101:108,0],pos_ds[101:108,1],pos_ds[101:108,2],color='yellow',label='CA3b')

dgg = ax.scatter(pos_ds[109:492,0],pos_ds[109:492,1],pos_ds[109:492,2],color='green',label='DGg')
dgh = ax.scatter(pos_ds[493:524,0],pos_ds[493:524,1],pos_ds[493:524,2],color='black',label='DGh')
dgb = ax.scatter(pos_ds[525:556,0],pos_ds[525:556,1],pos_ds[525:556,2],color='purple',label='DGb')

plt.title('Hippocampus')
plt.legend(handles=[ec,ca3e,ca3o,ca3b,dgg,dgh,dgb])
plt.show()