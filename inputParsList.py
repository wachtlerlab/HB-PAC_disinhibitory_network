from brian2 import units, array

period265 = (1 / 265)

onePulse = dict(nOutputs=1, sinPulseStarts=array([10]) * units.ms,
                sinPulseDurs=array([0.9 * period265]) * units.second)
twoPulse = dict(nOutputs=1, sinPulseStarts=array([10]) * units.ms,
                sinPulseDurs=array([1.9 * period265]) * units.second)
threePulse = dict(nOutputs=1, sinPulseStarts=array([10]) * units.ms,
                sinPulseDurs=array([2.9 * period265]) * units.second)
oneSecondPulse = dict(nOutputs=1, sinPulseStarts=array([10]) * units.ms,
                sinPulseDurs=array([1]) * units.second)
