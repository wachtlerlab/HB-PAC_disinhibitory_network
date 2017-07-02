import nixio
from dirDefs import homeFolder
import os
import seaborn as sns
from mplPars import mplPars
from brian2 import units
from matplotlib import pyplot as plt
from neoNIXIO import multiTag2SpikeTrain, dataArray2AnalogSignal, \
    simpleFloat, property2qu
import quantities as qu
from neo import AnalogSignal

mplPars['xtick.labelsize'] = 10
mplPars['ytick.labelsize'] = 10
mplPars["text.usetex"] = False
mplPars["font.sans-serif"] = "Arial"
mplPars["axes.linewidth"] = 1
sns.set(style="ticks", rc=mplPars)


simSettleTime = 600 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 150 * units.ms
# # inputParsName = 'onePulse'
# # inputParsName = 'twoPulse'
# # inputParsName = 'threePulse'
# inputParsName = "fortyMSPulse"
# showBefore = 50 * units.ms
# showAfter = 50 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 450 * units.ms
inputParsName = "pTShortInt33Dur16"
# inputParsName = "pTShortInt100Dur16"

showBefore = 75 * units.ms
showAfter = -30 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 1500 * units.ms
# # inputParsName = 'oneSecondPulse'
# # inputParsName = 'pulseTrainInt20Dur10'
# inputParsName = 'pulseTrainInt20Dur16'
# # inputParsName = 'pulseTrainInt33Dur10'
# # inputParsName = 'pulseTrainInt33Dur16'
# showBefore = 500 * units.ms
# showAfter = 500 * units.ms

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
OPNixFile = os.path.join(opDir, 'simResults.h5')


totalSimDur = simDuration + simSettleTime

nixFile = nixio.File.open(OPNixFile, nixio.FileMode.ReadOnly)

inputSec = nixFile.sections["Input Parameters"]
simSettleTimeQu = property2qu(inputSec.props["simSettleTime"])

blk = nixFile.blocks["Simulation Traces"]
dlint1MemV = blk.data_arrays["DLInt1 MemV"]
dlint1SpikesMT = blk.multi_tags["DLInt1 Spikes"]
dlint2MemV = blk.data_arrays["DLInt2 MemV"]
dlint2SpikesMT = blk.multi_tags["DLInt2 Spikes"]
sinInput = blk.data_arrays["Input Vibration Signal"]
joSpikesMT = blk.multi_tags["JO Spikes"]

dlint1MemVAS = dataArray2AnalogSignal(dlint1MemV)
dlint2MemVAS = dataArray2AnalogSignal(dlint2MemV)
temp = dataArray2AnalogSignal(sinInput)
sinInputAS = AnalogSignal(signal=15 * temp.magnitude,
                          units=temp.units,
                          t_start=temp.t_start,
                          sampling_period=temp.sampling_period)
sinInputAS = sinInputAS.reshape((sinInputAS.shape[0],))
dlint1SpikesST = multiTag2SpikeTrain(dlint1SpikesMT, sinInputAS.t_start, sinInputAS.t_stop)
dlint2SpikesST = multiTag2SpikeTrain(dlint2SpikesMT, sinInputAS.t_start, sinInputAS.t_stop)
joSpikesST = multiTag2SpikeTrain(joSpikesMT, sinInputAS.t_start, sinInputAS.t_stop)

# fig0, ax0 = plt.subplots(figsize=(2.5, 1.5))
# fig1, ax1 = plt.subplots(figsize=(2.5, 1.5))
# fig2, ax2 = plt.subplots(figsize=(2.5, 1.75))
#
fig0, ax0 = plt.subplots(figsize=(2.85, 1.5))
fig1, ax1 = plt.subplots(figsize=(2.85, 1.5))
fig2, ax2 = plt.subplots(figsize=(2.85, 1.75))

ax0.plot(simpleFloat((dlint1MemVAS.times - simSettleTimeQu) / qu.ms),
         simpleFloat(dlint1MemVAS / qu.mV), 'k-', lw=0.4)
ax1.plot(simpleFloat((dlint2MemVAS.times - simSettleTimeQu) / qu.ms),
         simpleFloat(dlint2MemVAS / qu.mV), 'k-', lw=0.4)
ax2.plot(simpleFloat((sinInputAS.times - simSettleTimeQu) / qu.ms),
         simpleFloat(sinInputAS / qu.um), 'k-', lw=0.4)

for ax in [ax0, ax1, ax2]:
    ax.set_xlim([(-showBefore) / units.ms,
                     (simDuration + showAfter) / units.ms])
    # ax.yaxis.tick_right()
    ax.set_xticks([])
    ax.set_ylim([-50, 5])
    ax.set_yticks([-40, -20, 0])
    # ax.set_yticks([])


for ax in [ax0, ax1]:
    markerline, stemlines, baseline \
        = ax.stem(simpleFloat((joSpikesST.times - simSettleTimeQu) / qu.ms),
                      [-42] * joSpikesST.shape[0],
                      linefmt='k-', markerfmt='None', basefmt='None',
                      bottom=-50)
    plt.setp(stemlines, lw=0.4)


markerline, stemlines, baseline \
        = ax2.stem(simpleFloat((joSpikesST.times - simSettleTimeQu) / qu.ms),
                      [25] * joSpikesST.shape[0],
                      linefmt='k-', markerfmt='None', basefmt='None',
                      bottom=17)
plt.setp(stemlines, lw=0.5)
ax2.set_ylim([-20, 25])
ax2.set_xticks([0, 100, 200, 300])

for fig in [fig0, fig1, fig2]:

    fig.tight_layout()

fig0.savefig(os.path.join(opDir, "DL-Int-1MemV.svg"), dpi=300,
             bbox_inches='tight', transparent=True)
fig1.savefig(os.path.join(opDir, "DL-Int-2MemV.svg"), dpi=300,
             bbox_inches='tight', transparent=True)
fig2.savefig(os.path.join(opDir, "InputSignal.svg"), dpi=300,
             bbox_inches='tight', transparent=True)

