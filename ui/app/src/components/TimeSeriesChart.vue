<script setup lang="ts">
import {ref, onMounted, defineProps, PropType, computed} from 'vue'
import {api} from 'src/boot/axios'
// import {merge} from 'src/utils'
import {Chart} from 'src/components/models'
import {useI18n} from 'vue-i18n'

const {t} = useI18n()

const props = defineProps({
    chart: {
        type: Object as PropType<Chart>,
        required: true,
    },
    height: {
        type: Number,
        default: 500,
    },
    last: {
        type: String,
        default: '5h',
    },
    resolution: {
        type: String,
        default: '1m',
    },
})

const loading = ref<boolean>(true)
const series = ref([])
const annotations = ref([])

const options = computed(() => {
    const opt = props.chart.config
    opt.annotations = {
        xaxis: annotations,
    }
    return opt
})

onMounted(async () => {
    try {
        const respSeries = await api.get('/api/measurement/apex/', {
            params: {
                entity: 'MAC',
                feature: props.chart.measurements.join(','),
                last: props.last,
                resolution: props.resolution,
            },
        })
        console.debug('chart', props.chart)
        console.debug('data', respSeries.data)
        series.value = respSeries.data.series
        annotations.value = respSeries.data.annotations
        // const respSwitches = await api.get('/api/switch/apex/', {
        //     params: {
        //         switch: props.chart.switches.join(','),
        //         last: props.last,
        //         resolution: props.resolution,
        //     },
        // })
        // const _options: object = {
        //     fillColor: '#B3F7CA',
        //     opacity: 0.4,
        //     label: {
        //         borderColor: '#B3F7CA',
        //         style: {
        //             fontSize: '10px',
        //             color: '#fff',
        //             background: '#00E396',
        //         },
        //         offsetY: -10,
        //     },
        // }
        // for (const item of respSwitches.data) {
        //     options.value?.annotations?.xaxis?.push(merge(item, _options))
        // }
    } catch (err) {
        console.error(err)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <q-spinner-dots v-if="loading" size="5em" />
    <apexchart
        v-else
        class="full-width"
        :height="props.height"
        :options="options"
        :series="series"></apexchart>
</template>

<style lang="sass">
.tooltip
  border: 1px solid #333
  border-radius: 5px
  padding: 3px
.tooltip > div:first-of-type
  background-color: rgb(237, 239, 241)
  border-radius: 5px 5px 0 0
  margin: -3px -3px 3px -3px
  padding: 3px
</style>
