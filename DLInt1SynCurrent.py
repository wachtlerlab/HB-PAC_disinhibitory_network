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

from neo import AnalogSignal
import nixio
from neoNIXIO import addAnalogSignal2Block, addMultiTag
import quantities as qu
from brianUtils import addBrianQuantity2Section


sns.set(style="whitegrid", rc=mplPars)


simSettleTime = 600 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 150 * units.ms
# inputParsName = 'onePulse'
# inputParsName = 'twoPulse'
# inputParsName = 'threePulse'
inputParsName = "fortyMSPulse"
showBefore = 300 * units.ms
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
DLInt1PropsDict = getattr(AdExpPars, DLInt1ModelProps)
dlint1 = VSNeuron(**AdExp, inits=DLInt1PropsDict, name='dlint1')
dlint1.recordMembraneV()
dlint1.recordSpikes()

DLInt1SynapsePropsE = 'DLInt1_syn_try2_e'
# DLInt1SynapsePropsE = ""
DLInt1SynapsePropsI = 'DLInt1_syn_try2_i'
# DLInt1SynapsePropsI = ""
DLInt1SynapseProps = "-".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))


opDir = os.path.join(homeFolder, DLInt1ModelProps, DLInt1SynapseProps, inputParsName)


opFile = os.path.join(opDir, 'SynCurrentTraces.png')
OPNixFile = os.path.join(opDir, 'simResWithSynCurrents.h5')
if os.path.isfile(opFile):
    ch = input('Results already exist at {}. Delete?(y/n):'.format(opFile))
    if ch == 'y':
        os.remove(opFile)
        if os.path.isfile(OPNixFile):
            os.remove(OPNixFile)
    else:
        sys.exit('User Abort!')

elif not os.path.isdir(opDir):
    os.makedirs(opDir)

inputPars = getattr(inputParsList, inputParsName)

JO = JOSpikes265(nOutputs=1, simSettleTime=simSettleTime, **inputPars)


if DLInt1SynapsePropsE:
    synPropsE = getattr(synapsePropsList, DLInt1SynapsePropsE)
    dlint1.addSynapse(synName="ExiJO", sourceNG=JO.JOSGG, **exp2Syn,
                      synParsInits=synPropsE,
                      synStateInits=exp2SynStateInits,
                      sourceInd=0, destInd=0
                      )

if DLInt1SynapsePropsI:
    synPropsI = getattr(synapsePropsList, DLInt1SynapsePropsI)
    dlint1.addSynapse(synName="InhJO", sourceNG=JO.JOSGG, **exp2Syn,
                      synParsInits=synPropsI,
                      synStateInits=exp2SynStateInits,
                      sourceInd=0, destInd=0
                      )

net = Network()
net.add(JO.JOSGG)
dlint1.addToNetwork(net)

if DLInt1SynapsePropsE:
    gEMonitor = StateMonitor(dlint1.incomingSynapses["ExiJO"], "g_ExiJO", record=True)
    net.add(gEMonitor)

if DLInt1SynapsePropsI:
    gIMonitor = StateMonitor(dlint1.incomingSynapses["InhJO"], "g_InhJO", record=True)
    net.add(gIMonitor)


defaultclock.dt = simStepSize
totalSimDur = simDuration + simSettleTime
net.run(totalSimDur, report='text')

simT, memV = dlint1.getMemVTrace()
spikeTimes = dlint1.getSpikes()

dlint1MemVAS = AnalogSignal(signal=memV / units.mV,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="mV",
                                name="DLInt1 MemV")


dlint1SpikesQU = (spikeTimes / units.ms) * qu.ms

joSpikesQU = (JO.spikeTimes / units.ms) * qu.ms

sineInput = getSineInput(simDur=simDuration, simStepSize=simStepSize,
                         sinPulseDurs=inputPars['sinPulseDurs'],
                         sinPulseStarts=inputPars['sinPulseStarts'],
                         freq=265 * units.Hz, simSettleTime=simSettleTime)

inputAS = AnalogSignal(signal=sineInput,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="um",
                                name="Input Vibration Signal")

fig, axs = plt.subplots(nrows=3, figsize=(10, 6.25), sharex='col')
axs[0].plot(simT / units.ms, memV / units.mV)
axs[0].set_ylabel('DLInt1\nMembrane\nPotential\n(mV)')
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
axs[0].plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
axs[0].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])
if DLInt1SynapsePropsE:
    gSynE = gEMonitor.g_ExiJO[0]
    iSynE = -gSynE * (memV - synPropsE['Esyn'])
    axs[1].plot(simT / units.ms,
                iSynE / units.nA, 'r-', label=r'$I_{synE}$')
    iSynEAS = AnalogSignal(signal=iSynE / units.nA,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="nA",
                                name="DL-Int-1 input EPSC")

if DLInt1SynapsePropsI:
    gSynI = gIMonitor.g_InhJO[0]
    iSynI = -gSynI * (memV - synPropsI['Esyn'])
    axs[1].plot(simT / units.ms,
                iSynI / units.nA, 'g-', label=r'$I_{synI}$')
    iSynIAS = AnalogSignal(signal=iSynI / units.nA,
                           sampling_period=(simStepSize / units.ms) * qu.ms,
                           t_start=0 * qu.mV,
                           units="nA",
                           name="DL-Int-1 input IPSC")

axs[1].legend(loc='center right')
axs[1].set_ylabel("Synaptic\ncurrents\n(nA)")

axs[2].plot(simT / units.ms, sineInput,
            color=[130. / 255, 72. / 255, 7. / 255], ls='-', marker='None',
            label='Vibration Input')
axs[2].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[2].legend(loc='upper right')
axs[2].set_xlabel('time (ms)')
axs[2].set_ylabel('Input')

fig.tight_layout()
fig.canvas.draw()
fig.savefig(opFile, dpi=150)

nixFile = nixio.File.open(OPNixFile, mode=nixio.FileMode.ReadWrite)
neuronModels = nixFile.create_section("Neuron Models", "Model Parameters")

DLInt1PropsSec = neuronModels.create_section("DL-Int-1", "AdExp")

for propName, propVal in DLInt1PropsDict.items():
    addBrianQuantity2Section(DLInt1PropsSec, propName, propVal)

inputSec = nixFile.create_section("Input Parameters", "Sinusoidal Pulses")

for parName, parVal in inputPars.items():
    addBrianQuantity2Section(inputSec, parName, parVal)

addBrianQuantity2Section(inputSec, "simSettleTime", simSettleTime)

brianSimSettingsSec = nixFile.create_section("Simulation Parameters", "Brian Simulation")
addBrianQuantity2Section(brianSimSettingsSec, "simStepSize", simStepSize)
addBrianQuantity2Section(brianSimSettingsSec, "totalSimDuration", totalSimDur)
brianSimSettingsSec.create_property("method", nixio.Value("euler"))


synPropsSec = nixFile.create_section("Synapse Models", "Model Parameters")

if DLInt1SynapsePropsE:

    JODLInt1SynESec = synPropsSec.create_section("JODLInt1Exi", "DoubleExpSyn")
    JODLInt1SynEDict = getattr(synapsePropsList, DLInt1SynapsePropsE)

    for propName, propVal in JODLInt1SynEDict.items():
        addBrianQuantity2Section(JODLInt1SynESec, propName, propVal)

    JODLInt1SynESec.create_property("PreSynaptic Neuron", nixio.Value("JO"))
    JODLInt1SynESec.create_property("PostSynaptic Neuron", nixio.Value("DLInt1"))


if DLInt1SynapsePropsI:

    JODLInt1SynISec = synPropsSec.create_section("JODLInt1Inh", "DoubleExpSyn")
    JODLInt1SynIDict = getattr(synapsePropsList, DLInt1SynapsePropsI)

    for propName, propVal in JODLInt1SynIDict.items():
        addBrianQuantity2Section(JODLInt1SynISec, propName, propVal)
    JODLInt1SynISec.create_property("PreSynaptic Neuron", nixio.Value("JO"))
    JODLInt1SynISec.create_property("PostSynaptic Neuron", nixio.Value("DLInt1"))

blk = nixFile.create_block("Simulation Traces", "Brian Output")
DLInt1DA = addAnalogSignal2Block(blk, dlint1MemVAS)
inputDA = addAnalogSignal2Block(blk, inputAS)
if DLInt1SynapsePropsE:
    epscAS = addAnalogSignal2Block(blk, iSynEAS)
if DLInt1SynapsePropsI:
    ipscAS = addAnalogSignal2Block(blk, iSynIAS)

addMultiTag("DLInt1 Spikes", type="Spikes", positions=dlint1SpikesQU,
            blk=blk, refs=[DLInt1DA])
addMultiTag("JO Spikes", type="Spikes", positions=joSpikesQU,
            blk=blk, refs=[inputDA])

nixFile.close()
