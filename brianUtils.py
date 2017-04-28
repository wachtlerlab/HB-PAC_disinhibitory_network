import numpy as np
from brian2.units.fundamentalunits import Quantity
import nixio

def getSimT(simDur: Quantity, simStepSize: Quantity) -> Quantity:

    return np.arange(simDur / simStepSize) * simStepSize

def addBrianQuantity2Section(sec: nixio.pycore.Section,
                             name: str, qu: Quantity) -> nixio.pycore.Property:

    propStr = qu.in_best_unit()
    propFloatStr, propUnit = propStr.split(" ")
    propFloat = float(propFloatStr)

    pr = sec.create_property(name, [nixio.Value(propFloat)])
    pr.unit = propUnitn

    return pr
