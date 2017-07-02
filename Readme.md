This repository contains the code used for the following manuscript:

Kumaraswamy et al. 2017, "Network simulations of interneuron circuits in the honeybee primary auditory center", bioarXiv

Authors:
Ajayrama Kumaraswamy, ajkumaraswamy@tutamail.com
Based on and contains parts of work by Aynur Maksutov during AMGEN program 2016 at Wachtlerlab, LMU.

Here is an overview of the contents:

.

+-- Ai2017Sim.yml: A file that can be used to create a conda environment to run the scripts below.

+-- models

|   +-- neuronModels.py: wrapper classes for brian2 neuron models

|   +-- neurons.py: Model equations and static parameters for neurons

|   +-- synapses.py: Model equations for synapses

|

+-- paramLists

|   +-- AdExpPars.py: Parameter combinations for the AdExp model

|   +-- inputParsList.py: Stimulii definitions

|   +-- synapsePropsList.py: Parameter combinations for the difference of exponential synaptic conductance model

|

+-- brianUtils.py: utility function related to brian2

|

+-- dirDefs.py: directory definitions imported in other scripts

|

+-- DLInt1SynCurrent.py: Script to simulate DL-Int-1 recording membrane potential and synaptic currents in NIX files

|

+-- DLInt2try.py: Legacy code

|

+-- forAi2017.py: Script to generate a subplot of an upcoming manuscript.

|

+-- JODLInt1DLInt2: Class to run network simulations

|

+-- justDLInt1.py: Legacy code

|

+-- mplPars.py: matplotlib rc parameters

|

+-- neoNIXIO.py: adapted from GJEMS, utility functions to work jointly with NIX and neo.

|

+-- plotDLInt1DLInt2SynEffects.py: script to plot summary of DL-Int-1 and DL-Int-2 responses to pulse trains.

|

+-- plotShortStims.py: script to plot summary of DL-Int-1 and DL-Int-2 responses to short continuous pulses.

|

+-- plotSynCurrents.py: script to plot membrane potential and synaptic currents of DL-Int-1 and DL-Int-2 for one stimulus.

|

+-- runJODLInt1DLInt2Multiple.py: script to simulate the network for multiple stimulii. Out is saved as a NIX File.

|

+-- simSynCurrents.py: script to simulate DL-Int-1 and DL-Int-2 recording membrane potential and synaptics currents in a NIXFile.

