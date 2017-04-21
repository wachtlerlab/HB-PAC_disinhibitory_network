from brian2 import units

exp2SynEqs = "\n".join((
    "g = B - A: siemens",
    "ISyn_post =  -g * (V_post - Esyn): amp (summed)",
    "dB/dt = -B/tau2: siemens (clock-driven)",
    "dA/dt = -A/tau1: siemens (clock-driven)",
    "tau1: second",
    "tau2: second",
    "wSyn: siemens",
    "Esyn: volt",
    ))

exp2Syn = {
    "model": exp2SynEqs,
    "on_pre": "A += wSyn\nB += wSyn",
}

exp2SynStateInits = {
    "A": 0 * units.siemens,
    "B": 0 * units.siemens
}