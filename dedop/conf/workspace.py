from .constants_reader import ConstantsFileReader
from typing import Optional

class WorkspaceConfig(ConstantsFileReader):
    @property
    def l1bs_output(self) -> Optional[str]:
        return self._data.get("l1bs_file")

    @property
    def l1b_output(self) -> str:
        return self["l1b_file"]

    @property
    def cnf_file(self) -> str:
        return self["cnf_file"]

    @property
    def cst_file(self) -> str:
        return self["cst_file"]

    @property
    def chd_file(self) -> str:
        return self["chd_file"]
