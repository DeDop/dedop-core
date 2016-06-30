from dedop.proc.sar.processor import L1BProcessor
from dedop.data.input.l1a import L1ADataset
from dedop.data.output import L1BWriter
from dedop.conf import CharacterisationFile, ConstantsFile, ConfigurationFile

cst = ConstantsFile("test_data/common/cst.json")
chd = CharacterisationFile(cst, "test_data/common/chd.json")
cnf = ConfigurationFile(
    zp_fact_range_cnf=2,
    min_lat_cnf=4.0,
    max_lat_cnf=5.0
)

l1a = L1ADataset(cst=cst, chd=chd, cnf=cnf, filename="../data/l1a/measurement_l1a.nc")
l1b = L1BWriter(chd=chd, cnf=cnf, filename="../data/output/l1b/measurement_l1b.nc")
l1b.create_all_dimensions()
l1b.create_all_variables()

with l1b as output:
    proc = L1BProcessor(l1a, chd_file=chd, cst_file=cst, l1b_output=output)
    proc.process()