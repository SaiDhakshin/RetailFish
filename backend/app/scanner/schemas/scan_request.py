from pydantic import BaseModel

from app.scanner.models.scan_filter import ScanFilter
from app.scanner.models.scan_universe import ScanUniverse


class ScanRequest(BaseModel):
    universe: ScanUniverse

    filters: list[ScanFilter]