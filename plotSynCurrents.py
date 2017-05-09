import nixio
from dirDefs import homeFolder
import os
import seaborn as sns
from mplPars import mplPars
from brian2 import units
from matplotlib import pyplot as plt
from neoNIXIO import multiTag2SpikeTrain, dataArray2AnalogSignal, simpleFloat
import quantities as qu

sns.set(style="whitegrid", rc=mplPars)


simSettleTime = 710 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 150 * units.ms
# inputParsName = 'onePulse'
# inputParsName = 'twoPulse'
# inputParsName = 'threePulse'
inputParsName = "fortyMSPulse"
showBefore = 50 * units.ms
showAfter = 50 * units.ms

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
OPNixFile = os.path.join(opDir, 'simResWithSynCurrents.h5')


totalSimDur = simDuration + simSettleTime

nixFile = nixio.File.open(OPNixFile, nixio.FileMode.ReadOnly)
blk = nixFile.blocks["Simulation Traces"]
dlint1MemV = blk.data_arrays["DLInt1 MemV"]
isynEDLInt1 = blk.data_arrays["DL-Int-1 input EPSC"]
isynIDLInt1 = blk.data_arrays["DL-Int-1 input IPSC"]
dlint1SpikesMT = blk.multi_tags["DLInt1 Spikes"]
dlint2MemV = blk.data_arrays["DLInt2 MemV"]
isynEDLInt2 = blk.data_arrays["DL-Int-2 input EPSC"]
isynIDLInt2 = blk.data_arrays["DL-Int-2 input IPSC"]
dlint2SpikesMT = blk.multi_tags["DLInt2 Spikes"]
sinInput = blk.data_arrays["Input Vibration Signal"]
joSpikesMT = blk.multi_tags["JO Spikes"]

dlint1MemVAS = dataArray2AnalogSignal(dlint1MemV)
isynEASDLInt1 = dataArray2AnalogSignal(isynEDLInt1)
isynIASDLInt1 = dataArray2AnalogSignal(isynIDLInt1)
dlint2MemVAS = dataArray2AnalogSignal(dlint2MemV)
isynEASDLInt2 = dataArray2AnalogSignal(isynEDLInt2)
isynIASDLInt2 = dataArray2AnalogSignal(isynIDLInt2)
sinInputAS = dataArray2AnalogSignal(sinInput)
dlint1SpikesST = multiTag2SpikeTrain(dlint1SpikesMT, sinInputAS.t_start, sinInputAS.t_stop)
dlint2SpikesST = multiTag2SpikeTrain(dlint2SpikesMT, sinInputAS.t_start, sinInputAS.t_stop)
joSpikesST = multiTag2SpikeTrain(joSpikesMT, sinInputAS.t_start, sinInputAS.t_stop)

fig1, ax1 = plt.subplots(nrows=2, figsize=(14, 11.2), sharex='col')
ax1[0].plot(simpleFloat(dlint1MemVAS.times / qu.ms),
            simpleFloat(dlint1MemVAS / qu.mV), 'b-')
markerline, stemlines, baseline \
    = ax1[0].stem(simpleFloat(joSpikesST.times / qu.ms),
                  [ax1[0].get_ylim()[1]] * joSpikesST.shape[0],
                  linefmt='r-.', markerfmt='None', basefmt='None',
                  bottom=ax1[0].get_ylim()[0])
plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)
ax1[0].axis('off')

ax1[1].plot(simpleFloat(isynEASDLInt1.times / qu.ms),
            simpleFloat(isynEASDLInt1 / qu.nA), color=[0, 0.6, 0],
            ls='-', marker='None')
ax1[1].plot(simpleFloat(isynIASDLInt1.times / qu.ms),
            simpleFloat(isynIASDLInt1 / qu.nA), color=[1, 0, 0],
            ls='-', marker='None')
markerline, stemlines, baseline \
    = ax1[1].stem(simpleFloat(joSpikesST.times / qu.ms),
                  [ax1[1].get_ylim()[1]] * joSpikesST.shape[0],
                  linefmt='r-.', markerfmt='None', basefmt='None',
                  bottom=ax1[1].get_ylim()[0])
plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)

ax1[1].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])
ax1[1].axis('off')

fig2, ax2 = plt.subplots(nrows=2, figsize=(14, 11.2), sharex='col')
ax2[0].plot(simpleFloat(dlint2MemVAS.times / qu.ms),
            simpleFloat(dlint2MemVAS / qu.mV), 'b-')
markerline, stemlines, baseline \
    = ax2[0].stem(simpleFloat(joSpikesST.times / qu.ms),
                  [ax2[0].get_ylim()[1]] * joSpikesST.shape[0],
                  linefmt='r-.', markerfmt='None', basefmt='None',
                  bottom=ax2[0].get_ylim()[0])
plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)
ax2[0].axis('off')

ax2[1].plot(simpleFloat(isynEASDLInt2.times / qu.ms),
            simpleFloat(isynEASDLInt2 / qu.nA), color=[0, 0.6, 0],
            ls='-', marker='None')
ax2[1].plot(simpleFloat(isynIASDLInt2.times / qu.ms),
            simpleFloat(isynIASDLInt2 / qu.nA), color=[1, 0, 0],
            ls='-', marker='None')
markerline, stemlines, baseline \
    = ax2[1].stem(simpleFloat(joSpikesST.times / qu.ms),
                  [ax2[1].get_ylim()[1]] * joSpikesST.shape[0],
                  linefmt='r-.', markerfmt='None', basefmt='None',
                  bottom=ax2[1].get_ylim()[0])
plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)

ax2[1].set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])
ax2[1].axis('off')

fig3, ax3 = plt.subplots(figsize=(14, 11.2))
ax3.plot(simpleFloat(sinInputAS.times / qu.ms),
         sinInputAS, 'k-')

ax3.set_xlim([(simSettleTime - showBefore) / units.ms,
                     (totalSimDur + showAfter) / units.ms])
markerline, stemlines, baseline \
    = ax3.stem(simpleFloat(joSpikesST.times / qu.ms),
                  [ax3.get_ylim()[1]] * joSpikesST.shape[0],
                  linefmt='r-.', markerfmt='None', basefmt='None',
                  bottom=ax3.get_ylim()[0])
plt.setp(stemlines, color=(0.5, 0.5, 0.5), lw=2)
ax3.axis('off')


for fig in [fig1, fig2, fig3]:
    fig.tight_layout()

fig1.savefig(os.path.join(opDir, "DL-Int-1memVSynCurrents.png"), dpi=150)
fig2.savefig(os.path.join(opDir, "DL-Int-2memVSynCurrents.png"), dpi=150)
fig3.savefig(os.path.join(opDir, "Input.png"), dpi=150)
