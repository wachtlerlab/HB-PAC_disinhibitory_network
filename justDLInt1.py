import os
import sys

import seaborn as sns
from brian2 import defaultclock, units
from matplotlib import pyplot as plt
from brian2.core.network import Network
from dirDefs import homeFolder
from models.neuronModels import VSNeuron, JOSpikes265, getSineInput
from models.neurons import AdExp
from models.synapses import exp2Syn, exp2SynStateInits
from mplPars import mplPars
from paramLists import synapsePropsList, inputParsList, AdExpPars

sns.set(style="whitegrid", rc=mplPars)


simSettleTime = 600 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 150 * units.ms
# # inputParsName = 'onePulse'
# # inputParsName = 'twoPulse'
# # inputParsName = 'threePulse'
# # inputParsName = "tenMSPulse"
# # inputParsName = "twentyMSPulse"
# # inputParsName = "thirtyMSPulse"
# inputParsName = "fortyMSPulse"
# # inputParsName = "fiftyMSPulse"
# showBefore = 50 * units.ms
# showAfter = 10 * units.ms


simStepSize = 0.1 * units.ms
simDuration = 1500 * units.ms
# inputParsName = 'pulseTrainInt20Dur10'
# inputParsName = 'pulseTrainInt20Dur16'
# inputParsName = 'pulseTrainInt33Dur16'
# inputParsName = 'pulseTrainInt33Dur10'
# inputParsName = 'oneSecondPulse'
# inputParsName = 'pulseTrainInt50Dur10'
inputParsName = 'pulseTrainInt50Dur16'
# inputParsName = 'pulseTrainInt50Dur20'
showBefore = 500 * units.ms
showAfter = 500 * units.ms

DLInt1ModelProps = "DLInt1Aynur"
dlint1 = VSNeuron(**AdExp, inits=getattr(AdExpPars, DLInt1ModelProps), name='dlint1')
dlint1.recordMembraneV()
dlint1.recordSpikes()

DLInt1SynapsePropsE = 'DLInt1_syn_try2_e'
# DLInt1SynapsePropsE = ""
DLInt1SynapsePropsI = 'DLInt1_syn_try2_i'
# DLInt1SynapsePropsI = ""
DLInt1SynapseProps = "-".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))


# opDir = os.path.join(homeFolder, DLInt1ModelProps, DLInt1SynapseProps, inputParsName)
opDir = "/tmp/justDLInt1"

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

JO = JOSpikes265(nOutputs=1, simSettleTime=simSettleTime, **inputPars)


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

net = Network()
net.add(JO.JOSGG)
dlint1.addToNetwork(net)
defaultclock.dt = simStepSize
totalSimDur = simDuration + simSettleTime
net.run(totalSimDur, report='text')

simT, memV = dlint1.getMemVTrace()
spikeTimes = dlint1.getSpikes()


fig, axs = plt.subplots(nrows=2, figsize=(10, 6.25), sharex='col')
axs[0].plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
axs[0].plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt1 \nmemV (mV)')
axs[0].set_xlim([(simSettleTime - showBefore) / units.ms,
                 (totalSimDur + showAfter) / units.ms])
sineInput = getSineInput(simDur=simDuration, simStepSize=simStepSize,
                         sinPulseDurs=inputPars['sinPulseDurs'],
                         sinPulseStarts=inputPars['sinPulseStarts'],
                         freq=265 * units.Hz, simSettleTime=simSettleTime)
axs[1].plot(simT / units.ms, sineInput, 'r-', label='Vibration Input')
axs[1].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[1].legend(loc='upper right')
axs[1].set_xlabel('time (ms)')
axs[1].set_ylabel('Vibration \nInput/JO\n Spikes')
fig.tight_layout()
fig.canvas.draw()
# plt.show()
fig.savefig(opFile, dpi=150)








