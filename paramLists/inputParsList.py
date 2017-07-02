from brian2 import units, array
from brian2.units.fundamentalunits import Quantity
import numpy as np

period265 = (1 / 265)

onePulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([0.9 * period265]) * units.second)
twoPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([1.9 * period265]) * units.second)
threePulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([2.9 * period265]) * units.second)

tenMSPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([10]) * units.ms)
twentyMSPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([20]) * units.ms)
thirtyMSPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([30]) * units.ms)
fortyMSPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([40]) * units.ms)
fiftyMSPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([50]) * units.ms)



oneSecondPulse = dict(sinPulseStarts=array([0]) * units.ms,
                sinPulseDurs=array([1]) * units.second)

def getPulseTrainInputPars(pulseDur: Quantity, pulseInt: Quantity,
                           stimDur: Quantity) -> dict:
    pulseDurF = float(pulseDur)
    pulseIntF = float(pulseInt)
    stimDurF = float(stimDur)

    sinPulseStarts = (np.arange(0, stimDurF, pulseIntF)) * units.second
    sinPulseDurs = ([pulseDurF] * len(sinPulseStarts)) * units.second

    return dict(sinPulseStarts=sinPulseStarts,
                sinPulseDurs=sinPulseDurs)

pulseTrainInt20Dur10 = getPulseTrainInputPars(pulseDur=10*units.ms, pulseInt=20*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt20Dur16 = getPulseTrainInputPars(pulseDur=16*units.ms, pulseInt=20*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt33Dur10 = getPulseTrainInputPars(pulseDur=10*units.ms, pulseInt=33*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt33Dur16 = getPulseTrainInputPars(pulseDur=16*units.ms, pulseInt=33*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt50Dur10 = getPulseTrainInputPars(pulseDur=10*units.ms, pulseInt=50*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt50Dur16 = getPulseTrainInputPars(pulseDur=16*units.ms, pulseInt=50*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt50Dur20 = getPulseTrainInputPars(pulseDur=20*units.ms, pulseInt=50*units.ms,
                                              stimDur=1*units.second)
pulseTrainInt50Dur30 = getPulseTrainInputPars(pulseDur=30*units.ms, pulseInt=50*units.ms,
                                              stimDur=1*units.second)
pTShortInt20Dur10 = getPulseTrainInputPars(pulseDur=10 * units.ms, pulseInt=20 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt20Dur16 = getPulseTrainInputPars(pulseDur=16 * units.ms, pulseInt=20 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt33Dur10 = getPulseTrainInputPars(pulseDur=10 * units.ms, pulseInt=33 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt33Dur16 = getPulseTrainInputPars(pulseDur=16 * units.ms, pulseInt=33 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt33Dur20 = getPulseTrainInputPars(pulseDur=20 * units.ms, pulseInt=33 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt50Dur10 = getPulseTrainInputPars(pulseDur=10 * units.ms, pulseInt=50 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt50Dur16 = getPulseTrainInputPars(pulseDur=16 * units.ms, pulseInt=50 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt50Dur20 = getPulseTrainInputPars(pulseDur=20 * units.ms, pulseInt=50 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt100Dur10 = getPulseTrainInputPars(pulseDur=10 * units.ms, pulseInt=100 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt100Dur16 = getPulseTrainInputPars(pulseDur=16 * units.ms, pulseInt=100 * units.ms,
                                           stimDur=250 * units.ms)
pTShortInt100Dur20 = getPulseTrainInputPars(pulseDur=20 * units.ms, pulseInt=100 * units.ms,
                                           stimDur=250 * units.ms)
