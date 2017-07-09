This repository contains the code used for the following manuscript:


Kumaraswamy, A., Maksutov, A., Kai, K., Ai, H., Ikeno, H., & Wachtler, T. (2017). Network simulations of interneuron circuits in the honeybee primary auditory center. *bioRxiv*. https://doi.org/10.1101/159533

Authors:
Ajayrama Kumaraswamy, ajkumaraswamy@tutamail.com
Based on and contains parts of work by Aynur Maksutov during AMGEN program 2016 at Wachtlerlab, LMU.

Installation:

With anaconda (recommended):

    1. conda create --name Ai2017Sim -c brian-team ipython>=6.1 numpy>=1.11.2 matplotlib>=1.5.3 seaborn>=0.7.1 brian2>=2.0.1 python>=3.5
    2. source activate Ai2017Sim (unix) or activate Ai2017Sim (windows)
    3. pip install <full path of this repository>

without anaconda, normal python installation required (https://www.python.org/)

    1. Install virtualenvwrapper (unix) or virtualenvwrapper-win (windows) be pre-installed with pip
    2. (only on windows) Install microsoft Visual C++ 14.0. Get it with "Microsoft Visual C++ Build Tools": http://landinghub.visualstudio.com/visual-cpp-build-tools
    3. mkvirtualenv Ai2017Sim
    4. pip install <full path of this repository>

Usage:
    1. source activate Ai2017Sim (unix) or activate Ai2017Sim (windows)
    2. Change the variable homeFolder in dirDefs.py to a folder. The results of the simulation will be stored here.
    3. The scripts of this repo are described below. All of them have some parameters at their top. Change these and run the scripts as needed.


Here is an overview of the contents:

.  
+-- Ai2017Sim.yml: A file that can be used to create a conda environment to run the scripts below. Essentially is a list of dependencies.
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
+-- DLInt1SynCurrent.py: Script to simulate DL-Int-1 recording membrane potential and synaptic currents in [NIX](https://github.com/G-Node/nixpy) files  
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
+-- neoNIXIO.py: adapted from GJEMS, utility functions to work jointly with [NIX](https://github.com/G-Node/nixpy) and [neo](https://github.com/NeuralEnsemble/python-neo).  
|  
+-- plotDLInt1DLInt2SynEffects.py: script to plot summary of DL-Int-1 and DL-Int-2 responses to pulse trains.  
|  
+-- plotShortStims.py: script to plot summary of DL-Int-1 and DL-Int-2 responses to short continuous pulses.  
|  
+-- plotSynCurrents.py: script to plot membrane potential and synaptic currents of DL-Int-1 and DL-Int-2 for one stimulus.  
|  
+-- runJODLInt1DLInt2Multiple.py: script to simulate the network for multiple stimulii. Out is saved as a [NIX](https://github.com/G-Node/nixpy) File.  
|  
+-- simSynCurrents.py: script to simulate DL-Int-1 and DL-Int-2 recording membrane potential and synaptics currents in a [NIX](https://github.com/G-Node/nixpy) file.  


