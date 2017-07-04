import nixio
from dirDefs import homeFolder
import os
import seaborn as sns
from mplPars import mplPars
from brian2 import units
from matplotlib import pyplot as plt
from neoNIXIO import multiTag2SpikeTrain, dataArray2AnalogSignal, simpleFloat
import quantities as qu

mplPars["axes.titlesize"] = 14
mplPars["font.size"] = 14
mplPars["xtick.labelsize"] = 12
mplPars["ytick.labelsize"] = 12
mplPars["legend.fontsize"] = 12
sns.set(rc=mplPars)


simSettleTime = 600 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 150 * units.ms
# # inputParsName = 'onePulse'
# # inputParsName = 'twoPulse'
# # inputParsName = 'threePulse'
# inputParsName = "thirtyMSPulse"
# # inputParsName = "fortyMSPulse"
#
# showBefore = 50 * units.ms
# showAfter = 0 * units.ms

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

simStepSize = 0.1 * units.ms
simDuration = 1500 * units.ms
inputParsName = 'oneSecondPulse'
# inputParsName = 'pulseTrainInt20Dur10'
# inputParsName = 'pulseTrainInt20Dur16'
# inputParsName = 'pulseTrainInt33Dur10'
# inputParsName = 'pulseTrainInt33Dur16'

showBefore = 500 * units.ms
showAfter = 0 * units.ms

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
OPNixFile = os.path.join(opDir, 'SimResults.h5')


totalSimDur = simDuration + simSettleTime

nixFile = nixio.File.open(OPNixFile, nixio.FileMode.ReadOnly)
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

fig1, axs1 = plt.subplots(nrows=2, figsize=(7, 4.375), sharex='col')
axs1[0].plot(simpleFloat(dlint1MemVAS.times / qu.ms),
                simpleFloat(dlint1MemVAS / qu.mV), 'b-', lw=0.5)
axs1[0].plot(simpleFloat(sinInputAS.times / qu.ms),
                simpleFloat((sinInputAS * 2.5 - 55 * qu.um) / qu.um),
               'k-', lw=0.5)
axs1[0].set_ylabel("DL-Int-1")
axs1[0].set_ylim([-60, 10])

axs1[1].plot(simpleFloat(dlint2MemVAS.times / qu.ms),
                simpleFloat(dlint2MemVAS / qu.mV), 'b-', lw=0.5)

axs1[1].plot(simpleFloat(sinInputAS.times / qu.ms),
                simpleFloat((sinInputAS * 2.5 - 55 * qu.um) / qu.um),
               'k-', lw=0.5)
axs1[1].set_ylabel("DL-Int-2")
# axs1[1].set_xlabel("Time (ms)")

axs1[1].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])
axs1[0].set_yticklabels([""] * len(axs1[1].get_yticks()))
axs1[1].set_yticklabels([""] * len(axs1[1].get_yticks()))
axs1[1].set_xticklabels([""] * len(axs1[1].get_xticks()))

for fig in [fig1]:
    fig.tight_layout()

fig1.savefig(os.path.join(opDir, "Traces.png"), dpi=300)
