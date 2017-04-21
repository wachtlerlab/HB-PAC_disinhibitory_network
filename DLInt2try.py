import os
import shutil

import seaborn as sns
from brian2 import defaultclock, units
from brian2.core.network import Network
from matplotlib import pyplot as plt

from dirDefs import homeFolder
from models.neuronModels import VSNeuron, JOSpikes265, getSineInput
from mplPars import mplPars
from paramLists import synapsePropsList, inputParsList

sns.set(style="whitegrid", rc=mplPars)


simSettleTime = 500 * units.ms

simStepSize = 0.5 * units.ms
simDuration = 100 * units.ms
# inputParsName = 'onePulse'
# inputParsName = 'twoPulse'
inputParsName = 'threePulse'


# simStepSize = 0.5 * units.ms
# simDuration = 1100 * units.ms
# # inputParsName = 'oneSecondPulse'
# # inputParsName = 'pulseTrainInt20Dur10'
# inputParsName = 'pulseTrainInt20Dur16'
# # inputParsName = 'pulseTrainInt33Dur10'
# # inputParsName = 'pulseTrainInt33Dur16'

NeuronProps = "DLInt2Try2"
NeuronSynapseProps = 'DLInt2_syn_try2'
dlint2 = VSNeuron(NeuronProps)

opDir = os.path.join(homeFolder, NeuronProps, NeuronSynapseProps, inputParsName)
if os.path.isdir(opDir):
    ch = input('Results already exist at {}. Delete?(y/n):'.format(opDir))
    if ch == 'y':
        shutil.rmtree(opDir)
os.makedirs(opDir)

period265 = (1 / 265)
inputPars = getattr(inputParsList, inputParsName)
JO = JOSpikes265(nOutputs=1, simSettleTime=simSettleTime, **inputPars)
dlint2.addExp2Synapses(name='JO', nSyn=1, sourceNG=JO.JOSGG,
                       sourceInd=0,
                       **getattr(synapsePropsList, NeuronSynapseProps))
net = Network()
net.add(JO.JOSGG)
dlint2.addToNetwork(net)
defaultclock.dt = simStepSize
totalSimDur = simDuration + simSettleTime
net.run(totalSimDur, report='text')

simT, memV = dlint2.getMemVTrace()
spikeTimes = dlint2.getSpikes()
fig, axs = plt.subplots(nrows=2, figsize=(10, 6.25), sharex='col')
axs[0].plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
axs[0].plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt1 \nmemV (mV)')
axs[0].set_xlim([simSettleTime / units.ms - 50, totalSimDur / units.ms + 50])

sineInput = getSineInput(simSettleTime=simSettleTime, simDur=simDuration,
                         simStepSize=simStepSize,
                         sinPulseDurs=inputPars['sinPulseDurs'],
                         sinPulseStarts=inputPars['sinPulseStarts'],
                         freq=265 * units.Hz)
axs[1].plot(simT / units.ms, sineInput, 'r-', label='Vibration Input')
axs[1].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[1].legend(loc='upper right')
axs[1].set_xlabel('time (ms)')
axs[1].set_ylabel('Vibration \nInput/JO\n Spikes')
fig.tight_layout()
fig.canvas.draw()
# plt.show()
fig.savefig(os.path.join(opDir, 'Traces.png'), dpi=150)
