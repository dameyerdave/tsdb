export interface ChartConfig {
    name: string
    config: object
}

export interface Chart {
    name: string
    measurements: Array<string>
    switches: Array<string>
    config: ChartConfig
}
