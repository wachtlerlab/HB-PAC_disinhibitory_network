import os
import sys

import seaborn as sns
from brian2 import defaultclock, units
from brian2.core.network import Network
from matplotlib import pyplot as plt

from dirDefs import homeFolder
from models.neuronModels import VSNeuron, JOSpikes265, getSineInput
from mplPars import mplPars
from paramLists import synapsePropsList, inputParsList, AdExpPars
from models.synapses import exp2SynStateInits, exp2Syn
from models.neurons import AdExp

sns.set(style="whitegrid", rc=mplPars)

simSettleTime = 500 * units.ms

simStepSize = 0.1 * units.ms
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


DLInt1ModelProps = "DLInt1Aynur"
dlint1 = VSNeuron(**AdExp, inits=getattr(AdExpPars, DLInt1ModelProps), name='dlint1')
dlint1.recordSpikes()
dlint1.recordMembraneV()

DLInt2ModelProps = "DLInt2Try2"
dlint2 = VSNeuron(**AdExp, inits=getattr(AdExpPars, DLInt2ModelProps), name='dlint2')
dlint2.recordMembraneV()
dlint2.recordSpikes()

DLInt1SynapsePropsE = 'DLInt1_syn_try2_e'
# DLInt1SynapsePropsE = ""
DLInt1SynapsePropsI = 'DLInt1_syn_try2_i'
# DLInt1SynapsePropsI = ""

DLInt1SynapseProps = "".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))

DLInt2SynapseProps = 'DLInt2_syn_try2'
# DLInt2SynapseProps = ""


# DLInt1DLInt2SynProps = "DLInt1_DLInt2_try1"
DLInt1DLInt2SynProps = ""

opDir = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                     DLInt1SynapseProps + DLInt2SynapseProps + DLInt1DLInt2SynProps,
                     inputParsName)
opFile = os.path.join(opDir, 'Traces.png')
if os.path.isfile(opFile):
    ch = input('Results already exist at {}. Delete?(y/n):'.format(opFile))
    if ch == 'y':
        os.remove(opFile)
    else:
        sys.exit('User Abort!')

elif not os.path.isdir(opDir):
    os.makedirs(opDir)

inputPars = getattr(inputParsList, inputParsName)

net = Network()
JO = JOSpikes265(nOutputs=1, simSettleTime=simSettleTime, **inputPars)
net.add(JO.JOSGG)

if DLInt1SynapsePropsE:
    dlint1.addSynapse(synName="ExiJO", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=getattr(synapsePropsList, DLInt1SynapsePropsE),
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )
if DLInt1SynapsePropsI:
    dlint1.addSynapse(synName="InhJO", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=getattr(synapsePropsList, DLInt1SynapsePropsI),
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )

dlint1.addToNetwork(net)

if DLInt2SynapseProps:
    dlint2.addSynapse(synName="JOExi", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=getattr(synapsePropsList, DLInt2SynapseProps),
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )

if DLInt1DLInt2SynProps:
    dlint2.addSynapse(synName="DLInt1", sourceNG=dlint1.ng, **exp2Syn,
                          synParsInits=getattr(synapsePropsList, DLInt1DLInt2SynProps),
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )


dlint2.addToNetwork(net)
defaultclock.dt = simStepSize
totalSimDur = simDuration + simSettleTime
net.run(totalSimDur, report='text')

simT, DLInt1_memV = dlint1.getMemVTrace()
DLInt1_spikeTimes = dlint1.getSpikes()
fig, axs = plt.subplots(nrows=3, figsize=(10, 6.25), sharex='col')
axs[0].plot(simT / units.ms, DLInt1_memV / units.mV)
spikesY = DLInt1_memV.min() + 1.05 * (DLInt1_memV.max() - DLInt1_memV.min())
axs[0].plot(DLInt1_spikeTimes / units.ms, [spikesY / units.mV] * DLInt1_spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt1 \nmemV (mV)')
axs[0].set_xlim([simSettleTime / units.ms - 50, totalSimDur / units.ms + 50])

simT, DLInt2_memV = dlint2.getMemVTrace()
DLInt2_spikeTimes = dlint2.getSpikes()
axs[1].plot(simT / units.ms, DLInt2_memV / units.mV)
spikesY = DLInt2_memV.min() + 1.05 * (DLInt2_memV.max() - DLInt2_memV.min())
axs[1].plot(DLInt2_spikeTimes / units.ms, [spikesY / units.mV] * DLInt2_spikeTimes.shape[0], 'k^')
axs[1].set_ylabel('DLInt2 \nmemV (mV)')

sineInput = getSineInput(simDur=simDuration, simStepSize=simStepSize,
                         sinPulseDurs=inputPars['sinPulseDurs'],
                         sinPulseStarts=inputPars['sinPulseStarts'],
                         freq=265 * units.Hz, simSettleTime=simSettleTime)
axs[2].plot(simT / units.ms, sineInput, 'r-', label='Vibration Input')
axs[2].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[2].legend(loc='upper right')
axs[2].set_xlabel('time (ms)')
axs[2].set_ylabel('Vibration \nInput/JO\n Spikes')
fig.tight_layout()
fig.canvas.draw()
# plt.show()
fig.savefig(os.path.join(opDir, 'Traces.png'), dpi=150)
