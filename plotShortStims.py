from brian2 import units
from matplotlib import pyplot as plt
import seaborn as sns
import os
from dirDefs import homeFolder
import nixio
from neoNIXIO import multiTag2SpikeTrain, dataArray2AnalogSignal, simpleFloat
import quantities as qu
from mplPars import mplPars

sns.set(rc=mplPars)
sns.axes_style('whitegrid')

simSettleTime = 600 * units.ms
#
simStepSize = 0.1 * units.ms
simDuration = 150 * units.ms
inputParsNames = {
                     10: "tenMSPulse",
                     20: "twentyMSPulse",
                     30: "thirtyMSPulse",
                     40: "fortyMSPulse"
                     }
showBefore = 50 * units.ms
showAfter = 50 * units.ms

totalSimDur = simSettleTime + simDuration

DLInt1ModelProps = "DLInt1Aynur"


DLInt2ModelProps = "DLInt2Try2"


DLInt1SynapsePropsE = 'DLInt1_syn_try2_e'
# DLInt1SynapsePropsE = ""
DLInt1SynapsePropsI = 'DLInt1_syn_try2_i'
# DLInt1SynapsePropsI = ""

DLInt2SynapseProps = 'DLInt2_syn_try2'
# DLInt2SynapseProps = ""


DLInt1DLInt2SynProps = "DLInt1_DLInt2_try1"
# DLInt1DLInt2SynProps = ""

DLInt1SynapseProps = "".join((DLInt1SynapsePropsE, DLInt1SynapsePropsI))

opDir = os.path.join(homeFolder, DLInt1ModelProps + DLInt2ModelProps,
                     DLInt1SynapseProps + DLInt2SynapseProps + DLInt1DLInt2SynProps)

fig, axs = plt.subplots(nrows=2, ncols=len(inputParsNames), figsize=(14, 11.2),
                        sharex='col')

for ipInd, (ipVal, ipName) in enumerate(inputParsNames.items()):

    nixFile = os.path.join(opDir, ipName, 'SimResults.h5')
    nixFile = nixio.File.open(nixFile, nixio.FileMode.ReadOnly)
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

    axs[0, ipInd].plot(simpleFloat(dlint1MemVAS.times / qu.ms),
                              simpleFloat(dlint1MemVAS / qu.mV), 'b-')
    # mew needs setting for seaborn. https://github.com/mwaskom/seaborn/issues/644
    axs[0, ipInd].plot(simpleFloat(dlint1SpikesST.times / qu.ms),
                              [4] * dlint1SpikesST.shape[0],
                              'b|', ms=8, mew=1)
    markerline, stemlines, baseline \
        = axs[0, ipInd].stem(simpleFloat(joSpikesST.times / qu.ms),
                      [-40] * joSpikesST.shape[0],
                      linefmt='r-.', markerfmt='None', basefmt='None',
                      bottom=-60)
    plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)
    axs[0, ipInd].plot(simpleFloat(sinInputAS.times / qu.ms),
                              simpleFloat(((5 * qu.um * sinInputAS) - 50 * qu.um) / qu.um)
                              , 'k-')
    # axs[0, ipInd].set_xlim([(simSettleTime - showBefore) / units.ms,
    #                                (totalSimDur + showAfter) / units.ms])
    axs[0, ipInd].set_ylim([-60, 10])
    axs[0, ipInd].yaxis.tick_right()


    axs[1, ipInd].plot(simpleFloat(dlint2MemVAS.times / qu.ms),
                       simpleFloat(dlint2MemVAS / qu.mV), 'b-')
    # mew needs setting for seaborn. https://github.com/mwaskom/seaborn/issues/644
    axs[1, ipInd].plot(simpleFloat(dlint2SpikesST.times / qu.ms),
                       [4] * dlint2SpikesST.shape[0],
                       'b|', ms=8, mew=1)
    markerline, stemlines, baseline \
        = axs[1, ipInd].stem(simpleFloat(joSpikesST.times / qu.ms),
                             [-40] * joSpikesST.shape[0],
                             linefmt='r-.', markerfmt='None', basefmt='None',
                             bottom=-60)
    plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)
    axs[1, ipInd].plot(simpleFloat(sinInputAS.times / qu.ms),
                       simpleFloat(((5 * qu.um * sinInputAS) - 50 * qu.um) / qu.um)
                       , 'k-')
    axs[1, ipInd].set_xlim([(simSettleTime - showBefore) / units.ms,
                            (totalSimDur + showAfter) / units.ms])
    axs[1, ipInd].set_ylim([-60, 10])
    axs[1, ipInd].yaxis.tick_right()

for ind in range(len(inputParsNames) - 1):
    axs[0, ind].set_yticks([])
    axs[1, ind].set_yticks([])

for ipInd, (ipVal, ipName) in enumerate(inputParsNames.items()):
    axs[0, ipInd].set_title(ipVal)

axs[0, 0].set_ylabel("DL-Int-1")
axs[1, 0].set_ylabel("DL-Int-2")

fig.tight_layout()
fig.savefig(os.path.join(opDir, "shortStims.png"), dpi=300)
