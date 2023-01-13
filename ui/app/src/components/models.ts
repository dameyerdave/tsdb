export interface ChartConfig {
    name: string
    config: object
}

export interface Chart {
    name: string
    sensors: Array<string>
    switches: Array<string>
    config: ChartConfig
}
