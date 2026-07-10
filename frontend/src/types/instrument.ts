export interface Instrument {
    id: number
    symbol: string
}

export interface InstrumentSearchResponse {
    total: number
    items: Instrument[]
}