import numpy as np
from brian2.units.fundamentalunits import Quantity

def getSimT(simDur: Quantity, simStepSize: Quantity) -> Quantity:

    return np.arange(int(simDur / simStepSize)) * simStepSize
