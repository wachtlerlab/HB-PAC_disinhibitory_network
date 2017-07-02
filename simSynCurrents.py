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
inputParsName = "thirtyMSPulse"
# inputParsName = "fortyMSPulse"
showBefore = 50 * units.ms
showAfter = 50 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 450 * units.ms
# # inputParsName = "pTShortInt20Dur10"
# # inputParsName = "pTShortInt20Dur16"
# # inputParsName = "pTShortInt33Dur10"
# # inputParsName = "pTShortInt33Dur16"
# # inputParsName = "pTShortInt33Dur20"
# # inputParsName = "pTShortInt50Dur10"
# # inputParsName = "pTShortInt50Dur16"
# # inputParsName = "pTShortInt50Dur20"
# inputParsName = "pTShortInt100Dur10"
# # inputParsName = "pTShortInt100Dur16"
# # inputParsName = "pTShortInt100Dur20"
#
# showBefore = 100 * units.ms
# showAfter = 100 * units.ms

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
opFileDLInt1 = os.path.join(opDir, 'SynCurrentTracesDLInt1.png')
opFileDLInt2 = os.path.join(opDir, 'SynCurrentTracesDLInt2.png')
OPNixFile = os.path.join(opDir, 'simResWithSynCurrents.h5')
if os.path.isfile(OPNixFile):
    ch = input('Results already exist at {}. Delete?(y/n):'.format(OPNixFile))
    if ch == 'y':
        os.remove(OPNixFile)
        if os.path.isfile(opFileDLInt1):
            os.remove(opFileDLInt1)
        if os.path.isfile(opFileDLInt2):
            os.remove(opFileDLInt2)
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
    synPropsEDLInt1 = getattr(synapsePropsList, DLInt1SynapsePropsE)
    dlint1.addSynapse(synName="ExiJO", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=synPropsEDLInt1,
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )
if DLInt1SynapsePropsI:
    synPropsIDLInt1 = getattr(synapsePropsList, DLInt1SynapsePropsI)
    dlint1.addSynapse(synName="InhJO", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=synPropsIDLInt1,
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )

dlint1.addToNetwork(net)

if DLInt1SynapsePropsE:
    gEMonitorDLInt1 = StateMonitor(dlint1.incomingSynapses["ExiJO"], "g_ExiJO", record=True)
    net.add(gEMonitorDLInt1)

if DLInt1SynapsePropsI:
    gIMonitorDLInt1 = StateMonitor(dlint1.incomingSynapses["InhJO"], "g_InhJO", record=True)
    net.add(gIMonitorDLInt1)

DLInt2PropsDict = getattr(AdExpPars, DLInt2ModelProps)
dlint2 = VSNeuron(**AdExp, inits=DLInt2PropsDict, name='dlint2')
dlint2.recordMembraneV()
dlint2.recordSpikes()

if DLInt2SynapseProps:
    synPropsEDLInt2 = getattr(synapsePropsList, DLInt2SynapseProps)
    dlint2.addSynapse(synName="ExiJO", sourceNG=JO.JOSGG, **exp2Syn,
                          synParsInits=synPropsEDLInt2,
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )

if DLInt1DLInt2SynProps:
    synPropsIDLInt2 = getattr(synapsePropsList, DLInt1DLInt2SynProps)
    dlint2.addSynapse(synName="DLInt1", sourceNG=dlint1.ng, **exp2Syn,
                          synParsInits=synPropsIDLInt2,
                          synStateInits=exp2SynStateInits,
                          sourceInd=0, destInd=0
                          )


dlint2.addToNetwork(net)

if DLInt2SynapseProps:
    gEMonitorDLInt2 = StateMonitor(dlint2.incomingSynapses["ExiJO"], "g_ExiJO", record=True)
    net.add(gEMonitorDLInt2)

if DLInt1DLInt2SynProps:
    gIMonitorDLInt2 = StateMonitor(dlint2.incomingSynapses["DLInt1"], "g_DLInt1", record=True)
    net.add(gIMonitorDLInt2)

defaultclock.dt = simStepSize
totalSimDur = simDuration + simSettleTime
net.run(totalSimDur, report='text')

simT, DLInt2memV = dlint2.getMemVTrace()
DLInt2spikeTimes = dlint2.getSpikes()

dlint2MemVAS = AnalogSignal(signal=DLInt2memV / units.mV,
                            sampling_period=(simStepSize / units.ms) * qu.ms,
                            t_start=0 * qu.mV,
                            units="mV",
                            name="DLInt2 MemV")

dlint2SpikesQU = (DLInt2spikeTimes / units.ms) * qu.ms

simT, DLInt1memV = dlint1.getMemVTrace()
DLInt1spikeTimes = dlint1.getSpikes()

dlint1MemVAS = AnalogSignal(signal=DLInt1memV / units.mV,
                            sampling_period=(simStepSize / units.ms) * qu.ms,
                            t_start=0 * qu.mV,
                            units="mV",
                            name="DLInt1 MemV")

dlint1SpikesQU = (DLInt1spikeTimes / units.ms) * qu.ms


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
axs[0].plot(simT / units.ms, DLInt2memV / units.mV)
spikesY = DLInt2memV.min() + 1.05 * (DLInt2memV.max() - DLInt2memV.min())
axs[0].plot(DLInt2spikeTimes / units.ms, [spikesY / units.mV] * DLInt2spikeTimes.shape[0], 'k^')
axs[0].set_ylabel('DLInt2\nMembrane\nPotential\n(mV)')
axs[0].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])

fig1, axs1 = plt.subplots(nrows=3, figsize=(10, 6.25), sharex='col')
axs1[0].plot(simT / units.ms, DLInt1memV / units.mV)
spikesY = DLInt1memV.min() + 1.05 * (DLInt1memV.max() - DLInt1memV.min())
axs1[0].plot(DLInt1spikeTimes / units.ms, [spikesY / units.mV] * DLInt1spikeTimes.shape[0], 'k^')
axs1[0].set_ylabel('DLInt1\nMembrane\nPotential\n(mV)')
axs1[0].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])

if DLInt2SynapseProps:
    gSynEDLInt2 = gEMonitorDLInt2.g_ExiJO[0]
    iSynEDLInt2 = -gSynEDLInt2 * (DLInt2memV - synPropsEDLInt2['Esyn'])
    axs[1].plot(simT / units.ms,
                iSynEDLInt2 / units.nA, 'm-', label=r'$I_{synE}$')
    iSynEASDLInt2 = AnalogSignal(signal=iSynEDLInt2 / units.nA,
                           sampling_period=(simStepSize / units.ms) * qu.ms,
                           t_start=0 * qu.mV,
                           units="nA",
                           name="DL-Int-2 input EPSC")

if DLInt1DLInt2SynProps:
    gSynI = gIMonitorDLInt2.g_DLInt1[0]
    iSynI = -gSynI * (DLInt2memV - synPropsIDLInt2['Esyn'])
    axs[1].plot(simT / units.ms,
                iSynI / units.nA, 'c-', label=r'$I_{synI}$')
    iSynIASDLInt2 = AnalogSignal(signal=iSynI / units.nA,
                           sampling_period=(simStepSize / units.ms) * qu.ms,
                           t_start=0 * qu.mV,
                           units="nA",
                           name="DL-Int-2 input IPSC")

axs[1].legend(loc='center right')
axs[1].set_ylabel("Synaptic\ncurrents\n(nA)")

axs[2].plot(simT / units.ms, sineInput,
            color=[130. / 255, 72. / 255, 7. / 255], ls='-', marker='None',
            label='Vibration Input')
axs[2].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs[2].legend(loc='center right')
axs[2].set_xlabel('time (ms)')
axs[2].set_ylabel('Input')
fig.tight_layout()
fig.canvas.draw()
# plt.show()
fig.savefig(opFileDLInt2, dpi=150)

if DLInt1SynapsePropsE:
    gSynEDLInt1 = gEMonitorDLInt1.g_ExiJO[0]
    iSynEDLInt1 = -gSynEDLInt1 * (DLInt1memV - synPropsEDLInt1['Esyn'])
    axs1[1].plot(simT / units.ms,
                iSynEDLInt1 / units.nA, 'r-', label=r'$I_{synE}$')
    iSynEASDLInt1 = AnalogSignal(signal=iSynEDLInt1 / units.nA,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="nA",
                                name="DL-Int-1 input EPSC")

if DLInt1SynapsePropsI:
    gSynIDLInt1 = gIMonitorDLInt1.g_InhJO[0]
    iSynIDLInt1 = -gSynIDLInt1 * (DLInt1memV - synPropsIDLInt1['Esyn'])
    axs1[1].plot(simT / units.ms,
                iSynIDLInt1 / units.nA, 'g-', label=r'$I_{synI}$')
    iSynIASDLInt1 = AnalogSignal(signal=iSynIDLInt1 / units.nA,
                           sampling_period=(simStepSize / units.ms) * qu.ms,
                           t_start=0 * qu.mV,
                           units="nA",
                           name="DL-Int-1 input IPSC")


axs1[1].legend(loc='center right')
axs1[1].set_ylabel("Synaptic\ncurrents\n(nA)")

axs1[2].plot(simT / units.ms, sineInput,
            color=[130. / 255, 72. / 255, 7. / 255], ls='-', marker='None',
            label='Vibration Input')
axs1[2].plot(JO.spikeTimes / units.ms, [sineInput.max() * 1.05] * len(JO.spikeTimes), 'k^',
        label='JO Spikes')
axs1[2].legend(loc='center right')
axs1[2].set_xlabel('time (ms)')
axs1[2].set_ylabel('Input')
fig1.tight_layout()
fig1.canvas.draw()
# plt.show()
fig1.savefig(opFileDLInt1, dpi=150)

nixFile = nixio.File.open(OPNixFile, mode=nixio.FileMode.ReadWrite)
neuronModels = nixFile.create_section("Neuron Models", "Model Parameters")

DLInt1PropsSec = neuronModels.create_section("DL-Int-1", "AdExp")

for propName, propVal in DLInt1PropsDict.items():
    addBrianQuantity2Section(DLInt1PropsSec, propName, propVal)

DLInt2PropsSec = neuronModels.create_section("DL-Int-2", "AdExp")

for propName, propVal in DLInt2PropsDict.items():
    addBrianQuantity2Section(DLInt2PropsSec, propName, propVal)

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

if DLInt2SynapseProps:

    JODLInt2SynESec = synPropsSec.create_section("JODLInt2Exi", "DoubleExpSyn")
    JODLInt2SynEDict = getattr(synapsePropsList, DLInt2SynapseProps)

    for propName, propVal in JODLInt2SynEDict.items():
        addBrianQuantity2Section(JODLInt2SynESec, propName, propVal)
    JODLInt2SynESec.create_property("PreSynaptic Neuron", nixio.Value("JO"))
    JODLInt2SynESec.create_property("PostSynaptic Neuron", nixio.Value("DLInt2"))

if DLInt1DLInt2SynProps:

    DLInt1DLInt2SynSec = synPropsSec.create_section("DLInt1DLInt2Inh", "DoubleExpSyn")
    DLInt1DLInt2SynDict = getattr(synapsePropsList, DLInt1DLInt2SynProps)

    for propName, propVal in DLInt1DLInt2SynDict.items():
        addBrianQuantity2Section(DLInt1DLInt2SynSec, propName, propVal)
    DLInt1DLInt2SynSec.create_property("PreSynaptic Neuron", nixio.Value("DLInt1"))
    DLInt1DLInt2SynSec.create_property("PostSynaptic Neuron", nixio.Value("DLInt2"))

blk = nixFile.create_block("Simulation Traces", "Brian Output")
DLInt2DA = addAnalogSignal2Block(blk, dlint2MemVAS)
DLInt1DA = addAnalogSignal2Block(blk, dlint1MemVAS)
inputDA = addAnalogSignal2Block(blk, inputAS)
if DLInt1SynapsePropsE:
    epscAS = addAnalogSignal2Block(blk, iSynEASDLInt1)
if DLInt1SynapsePropsI:
    ipscAS = addAnalogSignal2Block(blk, iSynIASDLInt1)
if DLInt2SynapseProps:
    epscAS = addAnalogSignal2Block(blk, iSynEASDLInt2)
if DLInt1DLInt2SynProps:
    ipscAS = addAnalogSignal2Block(blk, iSynIASDLInt2)

addMultiTag("DLInt2 Spikes", type="Spikes", positions=dlint2SpikesQU,
            blk=blk, refs=[DLInt2DA])
addMultiTag("DLInt1 Spikes", type="Spikes", positions=dlint1SpikesQU,
            blk=blk, refs=[DLInt2DA])
addMultiTag("JO Spikes", type="Spikes", positions=joSpikesQU,
            blk=blk, refs=[inputDA])

nixFile.close()