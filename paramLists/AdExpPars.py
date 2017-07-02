# Most of these parameters are part of the work by Aynur Makhsutov
# during AMGEN program 2016 at Wachtlerlab, LMU. The last few parameters sets
# that start with "DLInt" have been newly added.


from brian2 import nA, mV, ms, nS, pF, nF, uA, uF


resonator = {
    "b": 0.0805 * nA,
    "V":-70.4*mV,
    "sF": 2 * mV,
    "tau": 144 * ms,
    "EL": -70.6 * mV,
    "gL": 20 * nS,
    "C": 2810 * pF,
    "a": 8 * nS
}

integrator = {
    "b": 0.0805 * nA,
    "V":-70.4*mV,
    "sF": 2 * mV,
    "tau": 144 * ms,
    "EL": -70.6 * mV,
    "gL": 20 * nS,
    "C": 12 * nF,
    "a": 4 * nS
}

rebound = {
    "w": 0 * uA,
    "Vr": -60 * mV,  # -48.5*mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 720 * ms,
    "EL": -60 * mV,
    "gL": 30 * nS,
    "C": 281 * pF,
    "a": 80 * nS
}

bursting = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -70.4 * mV,
    "sF": 2 * mV,
    "tau": 144 * ms,
    "EL": -70.6 * mV,
    "gL": 30 * nS,
    "C": 281 * pF,
    "a": 4 * nS
}

bursting_rebound = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 720 * ms,
    "EL": -60 * mV,
    "gL": 30 * nS,
    "C": 281 * pF,
    "a": 80 * nS
}

bursting_rebound_low = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 720 * ms,
    "EL": -60 * mV,
    "gL": 30 * nS,
    "C": 281 * pF,
    "a": 30 * nS
}

bursting_rebound_high = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 720 * ms,
    "EL": -60 * mV,
    "gL": 30 * nS,
    "C": 281 * pF,
    "a": 150 * nS
}


perc = {
    "Vr": 0.1,
    "Vt": 0.1,
    "b": 0.99,
    "sF": 0.2,
    "tau": 0.6,
    "gL": 0.01,
    "C": 0.2,
    "a": 0.4
}

hopf_resonator = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 120 * ms,
    "EL": -60 * mV,
    "gL": 30 * nS,
    "C": 681 * pF,
    "a": 80 * nS
}

hopf_resonator2 = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 120 * ms,
    "EL": -60 * mV,
    "gL": 6 * nS,
    "C": 1200 * pF,
    "a": 80 * nS
}

saddle_resonator = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 12 * ms,
    "EL": -60 * mV,
    "gL": 30 * nS,
    "C": 800 * pF,
    "a": 30 * nS
}

saddle_resonator2 = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 12 * ms,
    "EL": -60 * mV,
    "gL": 3 * nS,
    "C": 800 * pF,
    "a": 30 * nS
}

saddle_integrator = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 12 * ms,
    "EL": -60 * mV,
    "gL": 40 * nS,
    "C": 1200 * pF,
    "a": 3 * nS
}

saddle_mixed = {
    "w": 0 * uA,
    "Vr": -47.4 * mV,
    "Vt": -50.4 * mV,
    "b": 0.0805 * nA,
    "V": -60 * mV,
    "sF": 2 * mV,
    "tau": 12 * ms,
    "EL": -60 * mV,
    "gL": 80 * nS,
    "C": 300 * pF,
    "a": 10 * nS
}

result13 = {
    "w": 0 * uA,
    "Vr": -62.8 * mV,
    "Vt": -49.2 * mV,
    "b": 1.41 * nA,
    "V": -60 * mV,
    "sF": 7.2 * mV,
    "tau": 600 * ms,
    "EL": -60 * mV,
    "gL": 80 * nS,
    "C": 276 * pF,
    "a": 1037 * nS
}

mean_24_08_2016 = {
    "w": 0 * uA,
    "Vr": -55.56 * mV,
    "Vt": -49.82 * mV,
    "b": 1.85 * nA,
    "V": -60 * mV,
    "sF": 6.69 * mV,
    "tau": 617.8 * ms,
    "EL": -60 * mV,
    "gL": 411.7 * nS,
    "C": 5242.8 * pF,
    "a": 923 * nS
}

std_inits = {
            "w": 0*uA,
            "Vr": -70.6 * mV,#-48.5*mV,
            "Vt": -50.4 * mV,
            "b": 0.0805 * nA,
            "V":-70.4 * mV,
            "sF": 2 * mV,
            "tau": 144 * ms,
            "EL": -70.6 * mV,
            "gL": 30 * nS,
            "C": 281 * pF,
            "a": 4 * nS,
            "Vp": -25 * mV,
    "I": 0 * nA
}

DLInt2Try1 = {
    "b": 0.0805 * nA,
    "V": -30*mV,
    "sF": 2 * mV,
    "tau": 5 * ms,
    "EL": -30 * mV,
    "gL": 200000 * nS,
    "C": 0.5 * uF,
    "a": 4 * nS,
    "Vr": -30 * mV,
    "Vt": -20 * mV,
    "Vp": -10 * mV
}

DLInt1Try1 = {
    "b": 0.0805 * nA,
    "V": -30*mV,
    "sF": 2 * mV,
    "tau": 1 * ms,
    "EL": -30 * mV,
    "gL": 200000 * nS,
    "C": 0.5 * uF,
    "a": 200000 * nS,
    "Vr": -30 * mV,
    "Vt": -15 * mV,
    "Vp": -5 * mV
}

DLInt1Try2 = {
    "b": 1.367 * nA,
    "V": -30*mV,
    "sF": 6 * mV,
    "tau": 100 * ms,
    "EL": -30 * mV,
    "gL": 200000 * nS,
    "C": 0.5 * uF,
    "a": 400000 * nS,
    "Vr": -30 * mV,
    "Vt": -25 * mV,
    "Vp": 0 * mV
}

DLInt1Aynur = {
    "b": 1 * nA,
    "V": -30 * mV,
    "sF": 6 * mV,
    "tau": 180 * ms,
    "EL": -30 * mV,
    "gL": 500 * nS,
    "C": 0.125 * nF,
    "a": 500 * nS,
    "Vr": -31 * mV,
    "Vt": -27.5 * mV,
    "Vp": 0 * mV
}

DLInt2Try2 = {
    "b": 1 * nA,
    "V": -30 * mV,
    "sF": 6 * mV,
    "tau": 0.08 * ms,
    "EL": -30 * mV,
    "gL": 500 * nS,
    "C": 0.125 * nF,
    "a": 500 * nS,
    "Vr": -31 * mV,
    "Vt": -27.5 * mV,
    "Vp": 0 * mV
}