from dedop.proc.sar.processor import L1BProcessor
from dedop.data.input.l1a import L1ADataset
from dedop.conf import CharacterisationFile, ConstantsFile

cst = ConstantsFile("test_data/common/cst.json")
chd = CharacterisationFile(cst, "test_data/common/chd.json")

l1a = L1ADataset(cst=cst, chd=chd, filename="../data/l1a/measurement_l1a.nc")

proc = L1BProcessor(l1a, chd_file=chd, cst_file=cst, l1b_output=None)
proc.process()