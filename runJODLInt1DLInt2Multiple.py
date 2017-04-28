from JODLInt1DLInt2 import runJODLInt1DLInt2
from brian2 import units

simSettleTime = 710 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 150 * units.ms
# inputParsName = 'onePulse'
# inputParsName = 'twoPulse'
# inputParsName = 'threePulse'
inputParsName = "tenMSPulse"
# inputParsName = "twentyMSPulse"
# inputParsName = "thirtyMSPulse"
# inputParsName = "fortyMSPulse"
# inputParsName = "fiftyMSPulse"
showBefore = 50 * units.ms
showAfter = 50 * units.ms

# simStepSize = 0.5 * units.ms
# simDuration = 1500 * units.ms
# # inputParsName = 'oneSecondPulse'
# inputParsName = 'pulseTrainInt33Dur10'
# # inputParsName = 'pulseTrainInt33Dur16'
# # inputParsName = 'pulseTrainInt20Dur10'
# # inputParsName = 'pulseTrainInt20Dur16'
# showBefore = 500 * units.ms
# showAfter = 500 * units.ms

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

runJODLInt1DLInt2(simStepSize, simDuration, simSettleTime,
                  inputParsName, showBefore, showAfter,
                  DLInt1ModelProps, DLInt2ModelProps,
                  DLInt1SynapsePropsE, DLInt1SynapsePropsI,
                  DLInt2SynapseProps, DLInt1DLInt2SynProps,
                  askReplace=False
                  )