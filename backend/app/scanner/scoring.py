from app.scanner.models.scan_filter import ScanFilter

FILTER_SCORES = {
    ScanFilter.EMA_ALIGNMENT: 20,
    ScanFilter.FIFTY_TWO_WEEK_HIGH: 25,
    ScanFilter.VOLUME_BREAKOUT: 20,
    ScanFilter.RELATIVE_STRENGTH: 15,
    ScanFilter.VCP: 40,
    ScanFilter.CUP_HANDLE: 50,
}