import os

import seaborn as sns
from brian2 import defaultclock, units, StateMonitor
from brian2.core.network import Network
from matplotlib import pyplot as plt

from dirDefs import homeFolder
from models.neuronModels import VSNeuron, JOSpikes265, getSineInput
from mplPars import mplPars
from paramLists import synapsePropsList, inputParsList

sns.set(style="whitegrid", rc=mplPars)


# simStepSize = 0.5 * units.ms
# simDuration = 600 * units.ms
# # inputParsName = 'onePulse'
# # inputParsName = 'twoPulse'
# inputParsName = 'threePulse'


simStepSize = 0.5 * units.ms
simDuration = 1600 * units.ms
# inputParsName = 'oneSecondPulse'
# inputParsName = 'pulseTrainInt20Dur10'
# inputParsName = 'pulseTrainInt20Dur16'
# inputParsName = 'pulseTrainInt33Dur10'
inputParsName = 'pulseTrainInt33Dur16'

DLInt1ModelProps = "DLInt1Aynur"
DLInt1SynapseProps = 'DLInt1_syn_try2'
dlint1 = VSNeuron(DLInt1ModelProps)

opDir = os.path.join(homeFolder, DLInt1ModelProps, DLInt1SynapseProps, inputParsName)
opFile = os.path.join(opDir, 'synCurrents.png')
if os.path.isfile(opFile):
    ch = input('Results already exist at {}. Delete?(y/n):'.format(opFile))
    if ch == 'y':
        os.remove(opFile)
elif not os.path.isdir(opDir):
    os.makedirs(opDir)

period265 = (1 / 265)
inputPars = getattr(inputParsList, inputParsName)
JO = JOSpikes265(nOutputs=1, **inputPars)
synProps = getattr(synapsePropsList, DLInt1SynapseProps)
weights = synProps['weight']
dlint1.addExp2Synapses(name='JO', nSyn=len(weights), sourceNG=JO.JOSGG,
                       sourceInd=0,
                       **getattr(synapsePropsList, DLInt1SynapseProps))

net = Network()
net.add(JO.JOSGG)
dlint1.addToNetwork(net)

gSynMonitor = StateMonitor(dlint1.incomingSynapses['JO'], 'g', record=True)
net.add(gSynMonitor)

defaultclock.dt = simStepSize
net.run(simDuration, report='text')

simT, memV = dlint1.getMemVTrace()
spikeTimes = dlint1.getSpikes()

gSynE = gSynMonitor[0].g
iSynE = -gSynE * (memV - synProps['Esyn'][0])
gSynI = gSynMonitor[1].g
iSynI = -gSynI * (memV - synProps['Esyn'][1])
fig, axs = plt.subplots(nrows=3, figsize=(10, 6.25), sharex='col')

axs[0].plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
axs[0].plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt1 \nmemV (mV)')
axs[0].set_xlim([450, simDuration / units.ms])

axs[1].plot((simT + synProps['delay'][0]) / units.ms,
            iSynE / units.nA, 'b-', label='Excitatory synaptic current (nA)')
axs[1].plot((simT + synProps['delay'][1]) / units.ms,
            iSynI / units.nA, 'r-', label='Inhibitory synaptic current (nA)')
axs[1].legend(loc='upper left')

sineInput = getSineInput(simDur=simDuration, simStepSize=simStepSize,
                         sinPulseDurs=inputPars['sinPulseDurs'],
                         sinPulseStarts=inputPars['sinPulseStarts'],
                         freq=265 * units.Hz)
axs[2].plot(simT / units.ms, sineInput, 'r-', label='Vibration Input')
axs[2].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[2].legend(loc='upper right')
axs[2].set_xlabel('time (ms)')
axs[2].set_ylabel('Vibration \nInput/JO\n Spikes')
fig.tight_layout()
fig.canvas.draw()
# plt.show()
fig.savefig(opFile, dpi=150)







