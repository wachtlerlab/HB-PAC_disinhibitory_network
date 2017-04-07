from brian2 import NeuronGroup, TimedArray, StateMonitor, SpikeMonitor
from brian2 import mA, mV, nF, pF, siemens
from brian2.core.network import Network
from . import AdExpPars
from typing import Union

AdExpEqs = "\n".join((
    "Ex = gL*sF*exp( (V - Vt)/sF ) : amp",
    "IL = gL*(EL - V) : amp",
    "dV/dt = (I + Ex - w)/C : volt",
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
        self.initSim()

    def initSim(self):

        for k, v in self.inits.items():
            setattr(self.ng, k, v)

class DLInt1(BaseModel):

    def __init__(self, pars: str = "result13", recordMemV: bool=True,
                 recordSpikes: bool=True):

        super().__init__()
        self.updateInits(getattr(AdExpPars, pars))
        if recordMemV:
            self.recordMembraneV()
        if recordSpikes:
            self.recordSpikes()


