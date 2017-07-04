from JODLInt1DLInt2 import runJODLInt1DLInt2
from brian2 import units

simSettleTime = 600 * units.ms

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
# ]
# showBefore = 50 * units.ms
# showAfter = 50 * units.ms

# simStepSize = 0.1 * units.ms
# simDuration = 450 * units.ms
# inputParsNames = [
#     "pTShortInt20Dur10",
#     "pTShortInt20Dur16",
#     "pTShortInt33Dur10",
#     "pTShortInt33Dur16",
#     "pTShortInt33Dur20",
#     "pTShortInt50Dur10",
#     "pTShortInt50Dur16",
#     "pTShortInt50Dur20",
#     "pTShortInt100Dur10",
#     "pTShortInt100Dur16",
#     "pTShortInt100Dur20",
# ]
# showBefore = 100 * units.ms
# showAfter = 100 * units.ms

simStepSize = 0.1 * units.ms
simDuration = 1500 * units.ms
inputParsNames = [
    'oneSecondPulse',
    # 'pulseTrainInt33Dur10',
    # 'pulseTrainInt33Dur16',
    # 'pulseTrainInt20Dur10',
    # 'pulseTrainInt20Dur16',
    # 'pulseTrainInt50Dur10',
    # 'pulseTrainInt50Dur16',
    # 'pulseTrainInt50Dur20',
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