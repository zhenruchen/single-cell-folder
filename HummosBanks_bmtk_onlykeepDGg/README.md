# HummosBanks-BMTK
A direct implementation of HummosEtAl2014 using BMTK
## Requirements
* Python (https://www.anaconda.com/distribution/)
* Neuron (https://www.neuron.yale.edu/neuron/)
* BMTK (https://github.com/AllenInstitute/bmtk)
* BMTools (https://github.com/tjbanks/bmtools)


## QuickStart Guide

### Easy

Run any seed using:
```
python seed_sweep.py 8888 0 simulation_config.json
```
Where 8888 is the seed, 0 is the experiment number, and simulation_config.json is the base simulation config to copy and make changes to.

This will set a seed, build the network, run the network, and convert the spike output to a format understood by the original Hummos Matlab code.

### Custom

1. Generate synapse config files from the original paper (**only done once**) [writes to ```./biophys_components/synaptic_models/```)]
```
python generate_synapses.py
```
2. Generate experiment input spike files (**only done once**) [writes to ```./input/```]
```
python generate_inputs.py
```
3. Build the network
```
python build_network.py
```
4. Run the network
```
python run_bionet.py
```

## Plots
Ensure that **BMTools** is installed, instructions in link above

1. Spike raster
```
python -m bmtools.plot raster
```
2. Positioning (3D plot)
```
python -m bmtools.plot positions --group-by pop_name --title Hippocampus
```
3. Connection totals, average convergence, average divergence
```
python -m bmtools.plot connection-total --sids pop_name --tid pop_name --title Hippocampus --no-prepend-pop
python -m bmtools.plot connection-convergence --sids pop_name --tid pop_name --title Hippocampus --no-prepend-pop
python -m bmtools.plot connection-divergence --sids pop_name --tid pop_name --title Hippocampus --no-prepend-pop
```

## Original Design Steps
1. Generate BMTK directory
```
mkdir network
python -m bmtk.utils.sim_setup -n ./network bionet
```
2. Delete all files in 
```
./biophys_components/mechanisms/modfiles
```
3. Copy all *.mod* files in HummosEtAl2014 into 
```
./biophys_components/mechanisms/modfiles
```
4. Compile using mknrndll, copy *nrnmech.dll* into 
```
./biophys_components/mechanisms/nrnmech.dll
```
5. Create the folder
```
./biophys_components/hoc_templates
```
6. Tell BMTK where to find hoc templates. Insert 

```
 "templates_dir":"$COMPONENTS_DIR/hoc_templates"
```
into the *components* section of *circuit_config.json* similar to the following:
```
,
  "components": {
    "morphologies_dir": "$COMPONENTS_DIR/morphologies",
    "synaptic_models_dir": "$COMPONENTS_DIR/synaptic_models",
    "mechanisms_dir": "$COMPONENTS_DIR/mechanisms",
    "biophysical_neuron_models_dir": "$COMPONENTS_DIR/biophysical_neuron_templates",
    "point_neuron_models_dir": "$COMPONENTS_DIR/point_neuron_templates",
    "templates_dir":"$COMPONENTS_DIR/hoc_templates"
  },
```
  7. Copy *Template.hoc* in HummosEtAl2014 into 
```
./biophys_components/hoc_templates
```

8. Edit *Template.hoc*
   1. Add the following lines near the top of each template definition
   ```
   public NumSoma
   NumSoma = 1
   
   public all, somatic, basal, apical, axonal
   objref all, somatic, basal, apical, axonal
   objref this

   all = new SectionList()
   somatic = new SectionList()
   basal = new SectionList()
   apical = new SectionList()
   axonal = new SectionList()

   for i=0,NumSoma soma[i] { all.append()
       somatic.append()} 

   ```
   2. Change soma objects to arrays
   ```
   create soma[NumSoma] //old: create soma
   ```
   3. Change all soma references to array references
   ```
   soma[0] { //old: soma {
   ```
   4. At the end of the *init* method call
   ```
   define_shape()
   ```
9. Create a *blank.swc* file in 
```
.\biophys_components\morphologies 
```
10. Create and develop *build_network.py*. See file for notes. 
    1.  General steps:
        1.  Build nodes
        2.  Define synaptic delays, init, min, max weights
        3.  Create edges
        4.  Create recurrent edges
    2.  Lessons learned
        1.  If you don't connect a set of nodes to something you may run into RuntimeError: generator raised StopIteration
        2.  Each connection needs a sec_id, and sec_x for id of the segment and location on the segment
11. Run python *build_network.py*
12. Edit *run_bionet.py* and include the following code at line 3 to load hoc templates properly.
```
from bmtk.simulator.bionet.default_setters.cell_models import loadHOC

bionet.pyfunction_cache.add_cell_model(loadHOC, directive='hoc', model_type='biophysical')

```
13. Edit *circuit_config* to reflect build parameters
```
"networks": {
    "nodes": [
      {
        "nodes_file": "$NETWORK_DIR\\hippocampus_nodes.h5",
        "node_types_file": "$NETWORK_DIR\\hippocampus_node_types.csv"
      }
    ],
    "edges": [
      {
        "edges_file": "$NETWORK_DIR\\hippocampus_hippocampus_edges.h5",
        "edge_types_file": "$NETWORK_DIR\\hippocampus_hippocampus_edge_types.csv" 
      }
    ]
  }
```
14. Run the following to run your network:
```
python run_bionet.py simulation_config.json
```
