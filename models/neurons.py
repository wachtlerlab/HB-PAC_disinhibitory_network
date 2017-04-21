AdExpEqs = "\n".join((
    "Ex = gL*sF*exp( (V - Vt)/sF ) : amp",
    "IL = gL*(EL - V) : amp",
    "dV/dt = (I + IL + Ex - w)/C : volt",
    "dw/dt = (a*(V - EL) - w)/tau : amp",
    "Vt : volt",
    "Vr : volt",
    "b : amp",
    "sF : volt",
    "tau: second",
    "EL : volt",
    "gL : siemens",
    "C : farad",
    "a : siemens",
    "Vp : volt"
    ))

AdExp = {"model": AdExpEqs,
         "threshold": "V > Vp",
         "reset": "V = Vr; w+=b"}