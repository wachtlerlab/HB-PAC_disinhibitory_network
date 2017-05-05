import nixio
from matplotlib import pyplot as plt
from brian2 import units
from dirDefs import homeFolder
import os
from neoNIXIO import dataArray2AnalogSignal, multiTag2SpikeTrain
from mplPars import mplPars
import seaborn as sns

sns.set(rc=mplPars)
sns.axes_style('whitegrid')

simStepSize = 0.5 * units.ms
simDuration = 1500 * units.ms
IntDurs = [
    (20, 10),
    (20, 16),
    (33, 10),
    (33, 16),
    (50, 10),
    (50, 16),
    (50, 20)
]

pulseInts = sorted(set([x[0] for x in IntDurs]))
pulseDurs = sorted(set([x[1] for x in IntDurs]))

showBefore = 500 * units.ms
showAfter = 500 * units.ms

DLInt1ModelProps = "DLInt1Aynur"


DLInt2ModelProps = "DLInt2Try2"


DLInt1SynapsePropsE = 'DLInt1_syn_try2_e'
# DLInt1SynapsePropsE = ""
DLInt1SynapsePropsI = 'DLInt1_syn_try2_i'
# DLInt1SynapsePropsI = ""

DLInt1SynapseProps = "".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))

DLInt2SynapseProps = 'DLInt2_syn_try2'
# DLInt2SynapseProps = ""


DLInt1DLInt2SynProps = "DLInt1_DLInt2_try1"
# DLInt1DLInt2SynProps = ""

fig1, axs1 = plt.subplots(nrows=len(pulseDurs), ncols=len(pulseInts), figsize=(14, 11.2))
fig2, axs2 = plt.subplots(nrows=len(pulseDurs), ncols=len(pulseInts), figsize=(14, 11.2))

for IntDur in IntDurs:

    pulseInt = IntDur[0]
    pulseDur = IntDur[1]
    inputParsName = 'pulseTrainInt{:d}Dur{:d}'.format(pulseInt, pulseDur)
    opDirWith = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                         DLInt1SynapseProps + DLInt2SynapseProps + DLInt1DLInt2SynProps,
                         inputParsName)
    OPNixFileWith = os.path.join(opDirWith, 'SimResults.h5')

    opDirWithout = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                             DLInt1SynapseProps + DLInt2SynapseProps,
                             inputParsName)
    OPNixFileWithout = os.path.join(opDirWithout, 'SimResults.h5')

    nixFile = nixio.File.open(OPNixFileWith, nixio.FileMode.ReadOnly)
    blk = nixFile.blocks["Simulation Traces"]
    dlint1MemV = blk.data_arrays["DLInt1 MemV"]
    dlint1SpikesMT = blk.multi_tags["DLInt1 Spikes"]
    dlint2MemV = blk.data_arrays["DLInt2 MemV"]
    dlint2SpikesMT = blk.multi_tags["DLInt2 Spikes"]
    sinInput = blk.data_arrays["Input Vibration Signal"]
    joSpikesMT = blk.multi_tags["JO Spikes"]

    dlint1MemVAS = dataArray2AnalogSignal(dlint1MemV)
    dlint2MemVAS = dataArray2AnalogSignal(dlint2MemV)
    sinInputAS = dataArray2AnalogSignal(sinInput)
    dlint1SpikesST = multiTag2SpikeTrain(dlint1SpikesMT, sinInputAS.t_start, sinInputAS.t_stop)
    dlint2SpikesST = multiTag2SpikeTrain(dlint2SpikesMT, sinInputAS.t_start, sinInputAS.t_stop)
    joSpikesST = multiTag2SpikeTrain(joSpikesMT, sinInputAS.t_start, sinInputAS.t_stop)

    nixFileWithout = nixio.File.open(OPNixFileWithout, nixio.FileMode.ReadOnly)
    blkWithout = nixFileWithout.blocks["Simulation Traces"]
    dlint2MemVWithout = blkWithout.data_arrays["DLInt2 MemV"]
    dlint2SpikesMTWithout = blkWithout.multi_tags["DLInt2 Spikes"]
    dlint2MemVASWithout = dataArray2AnalogSignal(dlint2MemVWithout)
    dlint2SpikesSTWithout = multiTag2SpikeTrain(dlint2SpikesMTWithout,
                                                sinInputAS.t_start, sinInputAS.t_stop)


    rowInd = pulseDurs.index(pulseDur)
    colInd = pulseInts.index(pulseInt)

    axs1[rowInd, colInd].plot(dlint1MemVAS.times, dlint1MemVAS, 'b-')
    spikesY = dlint1MemVAS.min() + 1.05 * (dlint1MemVAS.max() - dlint1MemVAS.min())
    axs1[rowInd, colInd].plot(dlint1SpikesST.times, [spikesY] * dlint1SpikesST.shape[0], 'b^')

    axs2[rowInd, colInd].plot(dlint2MemVAS.times, dlint2MemVAS, 'b-')
    axs2[rowInd, colInd].plot(dlint2MemVASWithout.times, dlint2MemVASWithout, 'r-')
    spikesY = dlint2MemVAS.min() + 1.05 * (dlint2MemVAS.max() - dlint2MemVAS.min())
    axs2[rowInd, colInd].plot(dlint2SpikesST.times, [spikesY] * dlint2SpikesST.shape[0], 'b^')
    spikesY = dlint2MemVAS.min() + 1.10 * (dlint2MemVAS.max() - dlint2MemVAS.min())
    axs2[rowInd, colInd].plot(dlint2SpikesSTWithout.times,
                              [spikesY] * dlint2SpikesSTWithout.shape[0], 'r^')

for ind, val in enumerate(pulseInts):

    axs1[0, ind].set_title(str(val))
    axs2[0, ind].set_title(str(val))

for ind, val in enumerate(pulseDurs):

    axs1[ind, 0].set_ylabel(str(val))
    axs2[ind, 0].set_ylabel(str(val))


fig1.tight_layout()
fig2.tight_layout()
fig1.savefig(os.path.join(homeFolder, 'DLInt1Summary.png'), dpi=150)
fig2.savefig(os.path.join(homeFolder, 'DLInt2Summary.png'), dpi=150)








