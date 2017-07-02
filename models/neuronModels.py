from copy import copy
from typing import Union, Iterable

import numpy as np
from brian2 import NeuronGroup, TimedArray, StateMonitor, SpikeMonitor, SpikeGeneratorGroup, array
from brian2 import Synapses
from brian2 import units
from brian2.core.network import Network
from brian2.equations.codestrings import CodeString
from brian2.equations.equations import Equations
from brian2.units.fundamentalunits import Quantity

from brianUtils import getSimT

def addSynNameVar(var: str, name: str) -> str:

    return "_".join([var, name])

def addSynNameEqs(model: str, prePosts: Iterable[Union[str, None]], synName: str) -> tuple:

    mEq = Equations(model)
    newM = copy(model)
    for name in mEq.names:
        if (not name.endswith("_post")) and (not name.endswith("_pre")):
            newM = newM.replace(name, addSynNameVar(name, synName))


    newPrePosts = []
    prePostCSs = []
    for p in prePosts:
        newP = copy(p)
        if p:
            cs = CodeString(p)
            for name in cs.identifiers:
                if (not name.endswith("_post")) and (not name.endswith("_pre")):
                    newP = newP.replace(name, addSynNameVar(name, synName))
            newPrePosts.append(newP)
            prePostCSs.append(cs)
        else:
            newPrePosts.append(None)
            prePostCSs.append(None)

    return newM, mEq, newPrePosts, prePostCSs


class VSNeuron(object):

    def __init__(self, model: str, name: str,
                 inits: dict,
                 threshold: str,
                 reset: str,
                 method: str = "euler"):

        super().__init__()
        self.ngParams = {"model": model, "threshold": threshold, "reset": reset, "method": method,
                         "name": name}
        self.inits = inits
        self.incomingSynapses = {}
        self.incomingSynapsePars = {}
        self.synCurrentNames = []
        self.recordMemVFlag = False
        self.recordSpikesFlag = False
        self.ng = None

    def updateInits(self, initUpdate: dict):

        self.inits.update(initUpdate)

    def setInputCurrent(self, I: Union[TimedArray, float]):
        self.inits["I"] = I

    def recordMembraneV(self):

        self.recordMemVFlag = True

    def recordSpikes(self):

        self.recordSpikesFlag = True

    def getMemVTrace(self):

        assert self.recordMemVFlag, 'Membrane Voltage was not recorded' \
                                            'for this neuron'
        return self.memVRecord.t, self.memVRecord[0].V

    def getSpikes(self):

        assert self.recordSpikesFlag, "Spikes were not recorded for this neuron"

        return self.spikeRecord.t

    def addToNetwork(self, network: Network):

        self.ngParams["model"] = "\n".join((self.ngParams["model"], "Iext: amp"))
        self.inits["Iext"] = 0 * units.amp
        eq2Add = "I = Iext "

        for synCurrentName in self.synCurrentNames:

            self.ngParams["model"] = "\n".join((self.ngParams["model"], "{} : amp".format(synCurrentName)))
            self.inits[synCurrentName] = 0 * units.amp
            eq2Add += " + {} ".format(synCurrentName)

        eq2Add += ": amp"

        self.ngParams["model"] = "\n".join((self.ngParams["model"], eq2Add))

        self.ng = NeuronGroup(N=1, **self.ngParams)
        self.initSim()
        network.add(self.ng)
        if self.recordMemVFlag:
            self.memVRecord = StateMonitor(self.ng, "V", record=[0])
            network.add(self.memVRecord)
        if self.recordSpikesFlag:
            self.spikeRecord = SpikeMonitor(self.ng)
            network.add(self.spikeRecord)

        for synName, synPars in self.incomingSynapsePars.items():

            syn = Synapses(synPars["source"], self.ng,
                           model=synPars["model"],
                           on_pre=synPars["on_pre"],
                           on_post=synPars["on_post"],
                           method=synPars["method"])

            syn.connect(i=synPars["sourceInd"], j=synPars["destInd"])

            for k, v in synPars["initMap"].items():

                setattr(syn, k, v)

            self.incomingSynapses[synName] = syn
            network.add(syn)


    def initSim(self):

        for k, v in self.inits.items():
            setattr(self.ng, k, v)

    def addSynapse(self, synName: str, sourceNG: NeuronGroup,
                   model: str, synParsInits: dict, synStateInits: dict,
                   on_pre: Union[str, None] = None,
                   on_post: Union[str, None] = None,
                   sourceInd: int = 0, destInd: int = 0,
                   method: str = "euler"):


        assert synName not in self.incomingSynapses, 'A Synapse with {} already exists'.format(synName)
        ISyn_PostInd = model.find("ISyn_post")
        assert ISyn_PostInd >= 0, "Synapse model should have an equation for" \
                                            "\'ISyn_post\'"
        nextEndLineInd = model.find("\n", ISyn_PostInd)
        assert model[nextEndLineInd - 8: nextEndLineInd] == "(summed)", \
            "Equation for \'ISyn_post\' must have (summed) flag"


        newModel, mEq, [newOn_pre, newOn_post], prePostCSs = \
            addSynNameEqs(model, [on_pre, on_post], synName)

        allSV = mEq.diff_eq_names
        allPars = list(mEq.parameter_names)


        for cs in prePostCSs:
            if cs:
                for i in cs.identifiers:
                    if i not in allSV:
                        allPars.append(i)

        for par in allPars:
            assert par in synParsInits, "Initialization not provided for {} in synParsInits".format(par)

        for sv in allSV:
            assert sv in synStateInits, "Initialization not provided for {} in synStateInits".format(sv)

        ISynName = "_".join(("ISyn", synName))
        self.synCurrentNames.append(ISynName)

        newModel = newModel.replace("ISyn", ISynName)

        initMap = {"delay": synParsInits["delay"]}
        for par in allPars:
            initMap[addSynNameVar(par, synName)] = synParsInits[par]

        for sv in allSV:
            initMap[addSynNameVar(sv, synName)] = synStateInits[sv]

        synPars = {"source": sourceNG, "model": newModel, "on_pre": newOn_pre,
                   "on_post": newOn_post, "method": method,
                   "sourceInd": sourceInd, "destInd": destInd, "initMap": initMap}

        self.incomingSynapsePars[synName] = synPars




class JOSpikes265(object):

    def __init__(self, nOutputs: int =1, simSettleTime: Quantity = 0 * units.ms,
                 sinPulseStarts: array = array(()) * units.ms,
                 sinPulseDurs: array = array(()) * units.ms):

        self.nOutputs = nOutputs
        freq = 265 * units.Hz
        spikePhase = np.deg2rad(240)
        phaseDelay = (1 / freq) * (spikePhase / (2 * np.pi))
        self.spikeTimes = []
        self.spikeInds = []
        simSettleTimeF = float(simSettleTime)

        for start, dur in zip(sinPulseStarts, sinPulseDurs):

            startF = float(start)
            durF = float(dur)
            periodF = float(1/freq)
            phaseDelayF = float(phaseDelay)

            cycleStarts = np.arange(startF, startF + durF, periodF)
            for i in range(nOutputs):
                self.spikeTimes += (simSettleTimeF + cycleStarts + phaseDelayF).tolist()
                self.spikeInds += [i] * len(cycleStarts)

        self.spikeTimes = self.spikeTimes * units.second
        self.JOSGG = SpikeGeneratorGroup(nOutputs, array(self.spikeInds),
                                         self.spikeTimes)

def getSineInput(simDur: Quantity, simStepSize: Quantity,
                 sinPulseStarts: Quantity, sinPulseDurs: Quantity,
                 freq: Quantity, simSettleTime: Quantity = 0 * units.ms,):

    simT = getSimT(simSettleTime + simDur, simStepSize)
    sineInput = np.zeros(simT.shape)

    for start, dur in zip(sinPulseStarts, sinPulseDurs):

        settleStart = start + simSettleTime
        settleEnd = start + dur + simSettleTime

        timeMask = (simT >= settleStart) & (simT <= settleEnd)
        sineInput[timeMask] = np.sin(2 * np.pi * freq * (simT[timeMask] - (0.5 / freq) - start))

    return sineInput




