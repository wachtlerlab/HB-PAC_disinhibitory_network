from models.neuronModels import DLInt1, JOSpikes265, getSineInput
from brian2 import defaultclock, units, TimedArray, SpikeGeneratorGroup, array
from brian2.core.network import Network
from matplotlib import pyplot as plt
import seaborn as sns
from mplPars import mplPars
import DLInt1SynapsePropsList
from dirDefs import homeFolder
import inputParsList
import os
import shutil


sns.set(style="whitegrid", rc=mplPars)


# simStepSize = 0.5 * units.ms
# simDuration = 200 * units.ms
# inputParsName = 'onePulse'
# inputParsName = 'twoPulse'
# inputParsName = 'threePulse'


simStepSize = 0.5 * units.ms
simDuration = 1200 * units.ms
inputParsName = 'oneSecondPulse'

DLInt1ModelProps = "DLInt1Aynur"
DLInt1SynapseProps = 'DLInt1_syn_try2'
dlint1 = DLInt1(DLInt1ModelProps)

opDir = os.path.join(homeFolder, DLInt1ModelProps, DLInt1SynapseProps, inputParsName)
if os.path.isdir(opDir):
    ch = input('Results already exist at {}. Delete?(y/n):'.format(opDir))
    if ch == 'y':
        shutil.rmtree(opDir)
os.makedirs(opDir)

period265 = (1 / 265)
inputPars = getattr(inputParsList, inputParsName)
JO = JOSpikes265(**inputPars)
dlint1.addExp2Synapses(name='JO', nSyn=2, sourceNG=JO.JOSGG,
                       sourceInd=0,
                       **getattr(DLInt1SynapsePropsList, DLInt1SynapseProps))
net = Network()
net.add(JO.JOSGG)
dlint1.addToNetwork(net)
defaultclock.dt = simStepSize
net.run(simDuration, report='text')

simT, memV = dlint1.getMemVTrace()
spikeTimes = dlint1.getSpikes()
fig, axs = plt.subplots(nrows=2, figsize=(10, 6.25), sharex='col')
axs[0].plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
axs[0].plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt1 \nmemV (mV)')

sineInput = getSineInput(simDur=simDuration, simStepSize=simStepSize,
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
plt.show()
# fig.savefig(os.path.join(opDir, 'Traces.png'), dpi=150)







