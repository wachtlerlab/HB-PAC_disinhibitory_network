from models.neuronModels import DLInt1
from brian2 import defaultclock, units, run
from brian2.core.network import Network
from matplotlib import pyplot as plt
import seaborn as sns
from mplPars import mplPars

sns.set(style="darkgrid", rc=mplPars)

dlint1 = DLInt1()
simStepSize = 0.5 * units.ms
simDuration = 100 * units.ms

dlint1.setInputCurrent(1 * units.nA)


net = Network()
dlint1.addToNetwork(net)
defaultclock.dt = simStepSize
net.run(simDuration, report='text')

simT, memV = dlint1.getMemVTrace()
spikeTimes = dlint1.getSpikes()
fig, ax = plt.subplots(figsize=(14, 11.2))
ax.plot(simT / units.ms, memV / units.mV)
spikesY = memV.min() + 1.05 * (memV.max() - memV.min())
ax.plot(spikeTimes / units.ms, [spikesY / units.mV] * spikeTimes.shape[0], 'k^')
ax.set_xlabel('time (ms)')
ax.set_ylabel('membrane potential (mV)')
plt.show()


