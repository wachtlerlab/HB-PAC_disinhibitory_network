from brian2 import NeuronGroup, TimedArray, StateMonitor, SpikeMonitor, SpikeGeneratorGroup, array
from brian2 import Synapses
from brian2.units.fundamentalunits import Quantity
from brian2 import units
from brian2.core.network import Network
from . import AdExpPars
from typing import Union
import numpy as np
from brianUtils import getSimT

AdExpEqs = "\n".join((
    "Ex = gL*sF*exp( (V - Vt)/sF ) : amp",
    "IL = gL*(EL - V) : amp",
    "dV/dt = (I + IL + Ex - w)/C : volt",
    "dw/dt = (a*(V - EL) - w)/tau : amp",
    "I: amp",
    "Vt : volt",
    "Vr : volt",
    "b : amp",
    "sF : volt",
    "tau: second",
    "EL : volt",
    "gL : siemens",
    "C : farad",
    "a : siemens",
    "Vp : volt"
    ))

exp2SynEqs = "\n".join((
    "g = B - A: siemens",
    "I_post = -g * (V_post - Esyn): amp (summed)"
    "dB/dt = -B/tau2: siemens (clock-driven)",
    "dA/dt = -A/tau1: siemens (clock-driven)",
    "tau1: second",
    "tau2: second",
    "w_pre: siemens",
    "Esyn: volt",
    ))

class BaseModel(object):

    def __init__(self, eqs: str = AdExpEqs,
                 inits: dict = AdExpPars.std_inits,
                 thresh: str = "V > Vp",
                 reset: str = "V = Vr; w+=b",
                 method: str = "euler"):

        super().__init__()
        self.ng = NeuronGroup(N=1, model=eqs, threshold=thresh,
                         reset=reset, method=method)
        self.inits = inits
        self.incomingSynapses = {}

    def updateInits(self, initUpdate: dict):

        self.inits.update(initUpdate)

    def setInputCurrent(self, I: Union[TimedArray, float]):
        self.inits["I"] = I

    def recordMembraneV(self):
        self.memVRecord = StateMonitor(self.ng, "V", record=[0])

    def recordSpikes(self):
        self.spikeRecord = SpikeMonitor(self.ng)

    def getMemVTrace(self):

        assert hasattr(self, "memVRecord"), 'Membrane Voltage was not recorded' \
                                            'for this neuron'
        return self.memVRecord.t, self.memVRecord[0].V

    def getSpikes(self):

        assert hasattr(self, "spikeRecord"), "Spikes were not recorded for this neuron"

        return self.spikeRecord.t

    def addToNetwork(self, network: Network):

        network.add(self.ng)
        if hasattr(self, "memVRecord"):
            network.add(self.memVRecord)
        if hasattr(self, "spikeRecord"):
            network.add(self.spikeRecord)

        for syn in self.incomingSynapses.values():
            network.add(syn)
        self.initSim()

    def initSim(self):

        for k, v in self.inits.items():
            setattr(self.ng, k, v)

    def addExp2Synapse(self, name: str, sourceNG: NeuronGroup,
                       weight: Quantity, Esyn: Quantity,
                       tau1: Quantity, tau2: Quantity, delay: Quantity,
                       sourceInd: int = 0):

        syn = Synapses(sourceNG, self.ng,
                 model=exp2SynEqs,
                 on_pre="A += w_pre\nB += w_pre",
                 delay=delay, method="euler")

        self.incomingSynapses[name] = syn
        syn.connect(i=sourceInd, j=0)
        syn.w_pre = weight
        syn.Esyn = Esyn
        syn.A = 0 * units.siemens
        syn.B = 0 * units.siemens
        syn.tau1 = tau1
        syn.tau2 = tau2

    def addExp2Synapses(self, name: str, nSyn: int, sourceNG: NeuronGroup,
                       weight: Quantity, Esyn: Quantity,
                       tau1: Quantity, tau2: Quantity, delay: Quantity,
                       sourceInd: int = 0):

        assert len(weight) == nSyn, "{} weights expected, {} were given".format(nSyn, nSyn + 1)
        assert len(Esyn) == nSyn, "{} Esyns expected, {} were given".format(nSyn, nSyn + 1)
        assert len(tau1) == nSyn, "{} tau1s expected, {} were given".format(nSyn, nSyn + 1)
        assert len(tau2) == nSyn, "{} tau2s expected, {} were given".format(nSyn, nSyn + 1)
        assert len(delay) == nSyn, "{} delays expected, {} were given".format(nSyn, nSyn + 1)

        syn = Synapses(sourceNG, self.ng,
                       model=exp2SynEqs,
                       on_pre="A += w_pre\nB += w_pre",
                       method="euler", multisynaptic_index='synInd')

        self.incomingSynapses[name] = syn
        syn.connect(i=sourceInd, j=0, n=2)

        syn.w_pre[0, 0, :] = weight
        syn.Esyn[0, 0, :] = Esyn
        syn.A[0, 0, :] = 0 * units.siemens
        syn.B[0, 0, :] = 0 * units.siemens
        syn.tau1[0, 0, :] = tau1
        syn.tau2[0, 0, :] = tau2


class DLInt1(BaseModel):

    def __init__(self, pars: str = "result13", recordMemV: bool=True,
                 recordSpikes: bool=True):

        super().__init__()
        self.updateInits(getattr(AdExpPars, pars))
        if recordMemV:
            self.recordMembraneV()
        if recordSpikes:
            self.recordSpikes()


class JOSpikes265(object):

    def __init__(self, nOutputs: int =1, sinPulseStarts: array = array(()) * units.ms,
                 sinPulseDurs: array = array(()) * units.ms):

        super().__init__()
        self.freq = 265 * units.Hz
        self.spikePhase = np.deg2rad(240)
        self.phaseDelay = (1 / self.freq) * (self.spikePhase / (2 * np.pi))
        self.spikeTimes = []
        self.spikeInds = []
        for start, dur in zip(sinPulseStarts, sinPulseDurs):

            startF = float(start)
            durF = float(dur)
            periodF = float(1/self.freq)
            phaseDelayF = float(self.phaseDelay)

            cycleStarts = np.arange(startF, startF + durF, periodF)
            for i in range(nOutputs):
                self.spikeTimes += (cycleStarts + phaseDelayF).tolist()
                self.spikeInds += [i] * len(cycleStarts)

        self.JOSGG = SpikeGeneratorGroup(nOutputs, array(self.spikeInds),
                                         array(self.spikeTimes) * units.second)

def getSineInput(simDur: Quantity, simStepSize: Quantity,
                 sinPulseStarts: Quantity, sinPulseDurs: Quantity, freq: Quantity):

    simT = getSimT(simDur, simStepSize)
    sineInput = np.zeros(simT.shape)

    for start, dur in zip(sinPulseStarts, sinPulseDurs):

        timeMask = (simT >= start) & (simT <= start + dur)
        sineInput[timeMask] = np.sin(2 * np.pi * freq * simT[timeMask])

    return sineInput




