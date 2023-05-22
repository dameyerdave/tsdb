export interface ChartConfig {
    annotations: object
}

export interface Chart {
    name: string
    measurements: Array<string>
    switches: Array<string>
    config: ChartConfig
}
