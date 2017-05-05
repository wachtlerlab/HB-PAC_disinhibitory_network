from JODLInt1DLInt2 import runJODLInt1DLInt2
from brian2 import units

simSettleTime = 710 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 150 * units.ms
# inputParsNames = [
#     'onePulse',
#     'twoPulse',
#     'threePulse',
#     "tenMSPulse",
#     "twentyMSPulse",
#     "thirtyMSPulse",
#     "fortyMSPulse",
#     "fiftyMSPulse",
# ]
#
# showBefore = 50 * units.ms
# showAfter = 50 * units.ms

simStepSize = 0.5 * units.ms
simDuration = 1500 * units.ms
inputParsNames = [
    'oneSecondPulse',
    'pulseTrainInt33Dur10',
    'pulseTrainInt33Dur16',
    'pulseTrainInt20Dur10',
    'pulseTrainInt20Dur16',
    'pulseTrainInt50Dur10',
    'pulseTrainInt50Dur16',
    'pulseTrainInt50Dur20',
    'pulseTrainInt50Dur30',
]

showBefore = 500 * units.ms
showAfter = 500 * units.ms

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

for inputParsName in inputParsNames:
    runJODLInt1DLInt2(simStepSize, simDuration, simSettleTime,
                      inputParsName, showBefore, showAfter,
                      DLInt1ModelProps, DLInt2ModelProps,
                      DLInt1SynapsePropsE, DLInt1SynapsePropsI,
                      DLInt2SynapseProps, DLInt1DLInt2SynProps,
                      askReplace=False
                      )