import nixio
from brian2 import units
from brianUtils import addBrianQuantity2Section

nf = nixio.File.open("/tmp/1.h5", nixio.FileMode.ReadWrite)
sec = nf.create_section("test", "Test")
addBrianQuantity2Section(sec, "Test", [1] * units.ms)