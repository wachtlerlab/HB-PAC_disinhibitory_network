import os
import sys

import seaborn as sns
from brian2 import defaultclock, units, StateMonitor
from matplotlib import pyplot as plt
from brian2.core.network import Network
from dirDefs import homeFolder
from models.neuronModels import VSNeuron, JOSpikes265, getSineInput
from models.neurons import AdExp
from models.synapses import exp2Syn, exp2SynStateInits
from mplPars import mplPars
from paramLists import synapsePropsList, inputParsList, AdExpPars

sns.set(style="whitegrid", rc=mplPars)


simSettleTime = 710 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 150 * units.ms
# inputParsName = 'onePulse'
# inputParsName = 'twoPulse'
# inputParsName = 'threePulse'
inputParsName = "fortyMSPulse"
showBefore = 50 * units.ms
showAfter = 50 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 1500 * units.ms
# # inputParsName = 'oneSecondPulse'
# # inputParsName = 'pulseTrainInt20Dur10'
# inputParsName = 'pulseTrainInt20Dur16'
# # inputParsName = 'pulseTrainInt33Dur10'
# # inputParsName = 'pulseTrainInt33Dur16'
# showBefore = 500 * units.ms
# showAfter = 500 * units.ms

DLInt1ModelProps = "DLInt1Aynur"

DLInt1SynapsePropsE = 'DLInt1_syn_try2_e'
# DLInt1SynapsePropsE = ""
DLInt1SynapsePropsI = 'DLInt1_syn_try2_i'
# DLInt1SynapsePropsI = ""
DLInt1SynapseProps = "".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))

DLInt2ModelProps = "DLInt2Try2"

DLInt2SynapseProps = 'DLInt2_syn_try2'

DLInt1DLInt2SynProps = "DLInt1_DLInt2_try1"

opDir = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                         DLInt1SynapseProps + DLInt2SynapseProps + DLInt1DLInt2SynProps,
                         inputParsName)
opFile = os.path.join(opDir, 'SynCurrentTraces.png')
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

DLInt1PropsDict = getattr(AdExpPars, DLInt1ModelProps)
dlint1 = VSNeuron(**AdExp, inits=DLInt1PropsDict, name='dlint1')
dlint1.recordSpikes()
dlint1.recordMembraneV()

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

DLInt2PropsDict = getattr(AdExpPars, DLInt2ModelProps)
dlint2 = VSNeuron(**AdExp, inits=DLInt2PropsDict, name='dlint2')
dlint2.recordMembraneV()
dlint2.recordSpikes()

if DLInt2SynapseProps:
    synPropsE = getattr(synapsePropsList, DLInt2SynapseProps)
    dlint2.addSynapse(synName="ExiJO", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=synPropsE,
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )

if DLInt1DLInt2SynProps:
    synPropsI = getattr(synapsePropsList, DLInt1DLInt2SynProps)
    dlint2.addSynapse(synName="DLInt1", sourceNG=dlint1.ng, **exp2Syn,
                          synParsInits=synPropsI,
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )


dlint2.addToNetwork(net)

if DLInt2SynapseProps:
    gEMonitor = StateMonitor(dlint2.incomingSynapses["ExiJO"], "g_ExiJO", record=True)
    net.add(gEMonitor)

if DLInt1DLInt2SynProps:
    gIMonitor = StateMonitor(dlint2.incomingSynapses["DLInt1"], "g_DLInt1", record=True)
    net.add(gIMonitor)




defaultclock.dt = simStepSize
totalSimDur = simDuration + simSettleTime
net.run(totalSimDur, report='text')

simT, memV = dlint2.getMemVTrace()
spikeTimes = dlint2.getSpikes()


fig, axs = plt.subplots(nrows=3, figsize=(10, 6.25), sharex='col')
axs[0].plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
axs[0].plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt2\nMembrane\nPotential\n(mV)')
axs[0].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])
sineInput = getSineInput(simDur=simDuration, simStepSize=simStepSize,
                         sinPulseDurs=inputPars['sinPulseDurs'],
                         sinPulseStarts=inputPars['sinPulseStarts'],
                         freq=265 * units.Hz, simSettleTime=simSettleTime)

if DLInt1SynapsePropsE:
    gSynE = gEMonitor.g_ExiJO[0]
    iSynE = -gSynE * (memV - synPropsE['Esyn'])
    axs[1].plot(simT / units.ms,
                iSynE / units.nA, 'm-', label=r'$I_{synE}$')

if DLInt1SynapsePropsI:
    gSynI = gIMonitor.g_DLInt1[0]
    iSynI = -gSynI * (memV - synPropsI['Esyn'])
    axs[1].plot(simT / units.ms,
                iSynI / units.nA, 'c-', label=r'$I_{synI}$')

axs[1].legend(loc='upper right')
axs[1].set_ylabel("Synaptic\ncurrents\n(nA)")

axs[2].plot(simT / units.ms, sineInput, color=[130. / 255, 72. / 255, 7. / 255], ls='-', marker='None',
            label='Vibration Input')
axs[2].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[2].legend(loc='upper right')
axs[2].set_xlabel('time (ms)')
axs[2].set_ylabel('Input')
fig.tight_layout()
fig.canvas.draw()
# plt.show()
fig.savefig(opFile, dpi=150)
