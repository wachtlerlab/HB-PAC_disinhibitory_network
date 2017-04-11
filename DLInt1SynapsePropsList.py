from brian2 import units
from dirDefs import homeFolder


DLInt1_syn_try1 = dict(weight=[5000, 400] * units.usiemens,
                    Esyn=[0, -80] * units.mvolt,
                    tau1=[4, 4] * units.ms, tau2=[4.5, 8] * units.ms,
                    delay=[6, 10] * units.ms)
DLInt1_syn_try2 = dict(weight=[18000, 1000] * units.nsiemens,
                    Esyn=[0, -80] * units.mvolt,
                    tau1=[4, 4] * units.ms, tau2=[4.5, 8] * units.ms,
                    delay=[6, 18] * units.ms)

