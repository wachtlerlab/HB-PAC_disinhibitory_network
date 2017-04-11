from models.neuronModels import DLInt1
from brian2 import defaultclock, units, TimedArray, SpikeGeneratorGroup, array
from brian2.core.network import Network
from matplotlib import pyplot as plt
import seaborn as sns
from mplPars import mplPars
import numpy as np
from brianUtils import getSimT

sns.set(style="darkgrid", rc=mplPars)


simStepSize = 0.5 * units.ms
simDuration = 500 * units.ms

dlint1 = DLInt1("DLInt2Try1")

# dlint1.setInputCurrent(1 * units.nA)
# simT = getSimT(simDuration, simStepSize)
# temp1 = 200 * units.ms <= simT
# temp2 = simT <= 350 * units.ms
# stepInputM = np.array(temp1 & temp2, dtype=float)
# stepInputM = stepInputM.reshape((stepInputM.shape[0], 1))
# stepInput = TimedArray(stepInputM, dt=simStepSize)
# dlint1.setInputCurrent(stepInput)

JOOutputSpikeTimes = array([100, 200]) * units.ms
jo = SpikeGeneratorGroup(1, array([0] * JOOutputSpikeTimes.shape[0]), JOOutputSpikeTimes)
dlint1.addExp2Synapse('JOInput', jo, weight=100 * units.usiemens, Esyn=0 * units.volt,
                      tau1=2 * units.ms, tau2=4 * units.ms, delay=5 * units.ms)

net = Network()
net.add(jo)
dlint1.addToNetwork(net)
defaultclock.dt = simStepSize
net.run(simDuration, report='text')

simT, memV = dlint1.getMemVTrace()
spikeTimes = dlint1.getSpikes()
fig, ax = plt.subplots(figsize=(10, 6.25))
ax.plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
ax.plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
ax.set_xlabel('time (ms)')
ax.set_ylabel('membrane potential (mV)')
plt.show()


