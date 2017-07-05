import nixio
from matplotlib import pyplot as plt
from brian2 import units
from dirDefs import homeFolder
import os
from neoNIXIO import dataArray2AnalogSignal, multiTag2SpikeTrain, simpleFloat
from mplPars import mplPars
import seaborn as sns
import quantities as qu

sns.set(rc=mplPars)


simSettleTime = 600 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 450 * units.ms
totalSimDur = simSettleTime + simDuration
IntDurs = [
    (20, 10),
    (20, 16),
    (33, 10),
    (33, 16),
    (33, 20),
    (50, 10),
    (50, 16),
    (50, 20),
    (100, 10),
    (100, 16),
    (100, 20)
]

pulseInts = sorted(set([x[0] for x in IntDurs]))
pulseDurs = sorted(set([x[1] for x in IntDurs]))

showBefore = 75 * units.ms
showAfter = -30 * units.ms

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

DLInt1SynapseProps = "".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))

opDir = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                     DLInt1SynapseProps + DLInt2SynapseProps + DLInt1DLInt2SynProps)

fig1, axs1 = plt.subplots(nrows=len(pulseDurs), ncols=len(pulseInts),
                          figsize=(14, 11.2), sharex='col')
fig2, axs2 = plt.subplots(nrows=len(pulseDurs), ncols=len(pulseInts),
                          figsize=(14, 11.2), sharex='col')

for IntDur in IntDurs:

    pulseInt = IntDur[0]
    pulseDur = IntDur[1]
    inputParsName = 'pTShortInt{:2d}Dur{:2d}'.format(pulseInt, pulseDur)
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

    axs1[rowInd, colInd].plot(simpleFloat(dlint1MemVAS.times / qu.ms),
                              simpleFloat(dlint1MemVAS / qu.mV), 'b-', lw=1)
    # mew needs setting for seaborn. https://github.com/mwaskom/seaborn/issues/644
    axs1[rowInd, colInd].plot(simpleFloat(dlint1SpikesST.times / qu.ms),
                              [4] * dlint1SpikesST.shape[0],
                              'b|', ms=8, mew=1)
    axs1[rowInd, colInd].plot(simpleFloat(sinInputAS.times / qu.ms),
                              simpleFloat(-50 + (sinInputAS * 5) / qu.um)
                              , 'k-', lw=1)
    axs1[rowInd, colInd].set_xlim([(simSettleTime - showBefore) / units.ms,
                                   (totalSimDur + showAfter) / units.ms])


    axs2[rowInd, colInd].plot(simpleFloat(dlint2MemVAS.times / qu.ms),
                              simpleFloat(dlint2MemVAS / qu.mV), 'b-', lw=1)
    axs2[rowInd, colInd].plot(simpleFloat(dlint2MemVASWithout.times / qu.ms),
                              simpleFloat(-45 + (dlint2MemVASWithout / qu.mV)),
                              'r-', lw=1)
    axs2[rowInd, colInd].plot(simpleFloat(dlint2SpikesST.times / qu.ms),
                              [12] * dlint2SpikesST.shape[0],
                            'b|', ms=8, mew=1)
    axs2[rowInd, colInd].plot(simpleFloat(dlint2SpikesSTWithout.times / qu.ms),
                              [6] * dlint2SpikesSTWithout.shape[0],
                              'r|', ms=8, mew=1)
    axs2[rowInd, colInd].plot(simpleFloat(sinInputAS.times / qu.ms),
                              simpleFloat(-105 + (sinInputAS * 7.5) / qu.um)
                              , 'k-', lw=1)
    axs2[rowInd, colInd].set_xlim([(simSettleTime - showBefore) / units.ms,
                                   (totalSimDur + showAfter) / units.ms])


for rowInd in range(axs1.shape[0]):
    for colInd in range(axs1.shape[1]):
        ax = axs1[rowInd, colInd]
        ax.set_ylim([-60, 10])
        ax.yaxis.tick_right()
        ax.set_yticklabels([""] * len(ax.get_yticks()))
        ax.set_xticklabels([""] * len(ax.get_xticks()))

for rowInd in range(axs2.shape[0]):
    for colInd in range(axs2.shape[1]):
        ax = axs2[rowInd, colInd]
        ax.set_ylim([-120, 20])
        ax.yaxis.tick_right()
        ax.set_yticklabels([""] * len(ax.get_yticks()))
        ax.set_xticklabels([""] * len(ax.get_xticks()))

for ind, val in enumerate(pulseInts):

    axs1[0, ind].set_title(str(val))
    axs2[0, ind].set_title(str(val))

for ind, val in enumerate(pulseDurs):

    axs1[ind, 0].set_ylabel(str(val))
    axs2[ind, 0].set_ylabel(str(val))

fig1.tight_layout()
fig2.tight_layout()

fig1.savefig(os.path.join(opDir, 'DLInt1Summary.png'), dpi=150)
fig2.savefig(os.path.join(opDir, 'DLInt2Summary.png'), dpi=150)









