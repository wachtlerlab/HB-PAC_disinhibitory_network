from brian2 import units

DLInt1_syn_try1 = dict(wSyn=[5000, 400] * units.usiemens,
                    Esyn=[0, -80] * units.mvolt,
                    tau1=[4, 4] * units.ms, tau2=[4.5, 8] * units.ms,
                    delay=[6, 10] * units.ms)
DLInt1_syn_try2 = dict(wSyn=[15000, 1500] * units.nsiemens,
                    Esyn=[0, -80] * units.mvolt,
                    tau1=[4, 4] * units.ms, tau2=[4.5, 8] * units.ms,
                    delay=[6, 18] * units.ms)

DLInt1_syn_try2_e = dict(wSyn=150 * units.nsiemens,
                    Esyn=0 * units.mvolt,
                    tau1=0.5 * units.ms, tau2=4 * units.ms,
                    delay=5 * units.ms)

DLInt1_syn_try2_i = dict(wSyn=5000 * units.nsiemens,
                    Esyn=-80 * units.mvolt,
                    tau1=4.8 * units.ms, tau2=5 * units.ms,
                    delay=10 * units.ms)

DLInt2_syn_try2 = dict(wSyn=400 * units.nsiemens,
                    Esyn=0 * units.mvolt,
                    tau1=0.5 * units.ms, tau2=4 * units.ms,
                    delay=5 * units.ms)

DLInt1_DLInt2_try1 = dict(wSyn=12000 * units.nsiemens,
                    Esyn=-80 * units.mvolt,
                    tau1=4.8 * units.ms, tau2=5 * units.ms,
                    delay=3 * units.ms)
