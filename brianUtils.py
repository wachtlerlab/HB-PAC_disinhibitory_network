import numpy as np
from brian2.units.fundamentalunits import Quantity
import nixio

def getSimT(simDur: Quantity, simStepSize: Quantity) -> Quantity:

    return np.arange(simDur / simStepSize) * simStepSize

def addBrianQuantity2Section(sec: nixio.pycore.Section,
                             name: str, qu: Quantity) -> nixio.pycore.Property:
    propStr = qu.in_best_unit()

    if qu.shape == ():

        propFloatStr, propUnit = propStr.split(" ")
        propFloat = float(propFloatStr)

        pr = sec.create_property(name, [nixio.Value(propFloat)])

    elif len(qu.shape) == 1:

        propFloatStr, propUnit = propStr.split("] ")
        values = list(map(float, propFloatStr[2:].split()))
        pr = sec.create_property(name, [nixio.Value(val) for val in values])

    else:
        raise(ValueError("Only scalar or 1D Brian Quantities as supported"))

    pr.unit = propUnit

    return pr
