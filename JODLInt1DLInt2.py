import os
import sys

import seaborn as sns
from brian2 import defaultclock, units
from brian2.core.network import Network
from brian2.units.fundamentalunits import Quantity
from matplotlib import pyplot as plt

from dirDefs import homeFolder
from models.neuronModels import VSNeuron, JOSpikes265, getSineInput
from mplPars import mplPars
from paramLists import synapsePropsList, inputParsList, AdExpPars
from models.synapses import exp2SynStateInits, exp2Syn
from models.neurons import AdExp

from neo import AnalogSignal, SpikeTrain
import nixio
from neoNIXIO import addAnalogSignal2Block, addMultiTag
import quantities as qu
from brianUtils import addBrianQuantity2Section


def runJODLInt1DLInt2(simStepSize: Quantity, simDuration: Quantity, simSettleTime: Quantity,
                      inputParsName: str, showBefore: Quantity, showAfter: Quantity,
                      DLInt1ModelProps: str, DLInt2ModelProps: str,
                      DLInt1SynapsePropsE: str, DLInt1SynapsePropsI: str,
                      DLInt2SynapseProps: str, DLInt1DLInt2SynProps: str,
                      askReplace=True):

    sns.set(style="whitegrid", rc=mplPars)

    DLInt1SynapseProps = "".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))

    opDir = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                         DLInt1SynapseProps + DLInt2SynapseProps + DLInt1DLInt2SynProps,
                         inputParsName)
    opFile = os.path.join(opDir, 'Traces.png')
    OPNixFile = os.path.join(opDir, 'SimResults.h5')

    if askReplace:
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
    else:
        if os.path.isfile(opFile):
            os.remove(opFile)
            if os.path.isfile(OPNixFile):
                os.remove(OPNixFile)

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
    axs[0].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])

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
    fig.savefig(opFile, dpi=150)
    plt.close(fig.number)
    del fig

    dlint1MemVAS = AnalogSignal(signal=DLInt1_memV /units.mV,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="mV",
                                name="DLInt1 MemV")
    dlint2MemVAS = AnalogSignal(signal=DLInt2_memV / units.mV,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="mV",
                                name="DLInt2 MemV")
    inputAS = AnalogSignal(signal=sineInput,
                                sampling_period=(simStepSize / units.ms) * qu.ms,
                                t_start=0 * qu.mV,
                                units="um",
                                name="Input Vibration Signal")
    dlint1SpikesQU = (DLInt1_spikeTimes / units.ms) * qu.ms
    dlint2SpikesQU = (DLInt2_spikeTimes / units.ms) * qu.ms
    joSpikesQU = (JO.spikeTimes / units.ms) * qu.ms

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
    DLInt1DA = addAnalogSignal2Block(blk, dlint1MemVAS)
    DLInt2DA = addAnalogSignal2Block(blk, dlint2MemVAS)
    inputDA = addAnalogSignal2Block(blk, inputAS)
    addMultiTag("DLInt1 Spikes", type="Spikes", positions=dlint1SpikesQU,
                blk=blk, refs=[DLInt1DA])
    addMultiTag("DLInt2 Spikes", type="Spikes", positions=dlint2SpikesQU,
                blk=blk, refs=[DLInt2DA])
    addMultiTag("JO Spikes", type="Spikes", positions=joSpikesQU,
                blk=blk, refs=[inputDA])


    nixFile.close()



