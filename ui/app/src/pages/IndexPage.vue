<script setup lang="ts">
import ApexCharts from 'apexcharts'
import { ref, onMounted } from 'vue'
import { api } from 'src/boot/axios'
import { merge } from 'src/utils'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()

const CHART_HEIGHT = 350

const loading = ref<boolean>(true)

const options = ref<ApexCharts.ApexOptions>({
  chart: {
    type: 'line',
    zoom: {
      type: 'x',
      enabled: true,
      autoScaleYaxis: true
    },
    animations: {
      enabled: false
    },
    dropShadow: {
      enabled: true,
      color: '#000',
      top: 18,
      left: 7,
      blur: 10,
      opacity: 0.2
    },
    stacked: false
  },
  dataLabels: {
    enabled: false
  },
  markers: {
    size: 0,
  },
  stroke: {
    curve: 'smooth'
  },
  title: {
    text: 'Sensor',
    align: 'left'
  },
  grid: {
    row: {
      colors: ['#f3f3f3', 'transparent'], // takes an array which will be repeated on columns
      opacity: 0.5
    },
  },
  tooltip: {
    x: {
      format: 'yyyy-MM-dd HH:mm:ss'
    }
  },
  noData: {
    text: t('message.loading')
  },
  legend: {
    position: 'top',
    horizontalAlign: 'center',
    floating: true,
    offsetY: -20,
    offsetX: -5
  },
  annotations: {
    xaxis: []
  },
  xaxis: {
    type: 'datetime'
  },
  yaxis: [
    {
      title: {
        text: 'Temperature',
        style: {
          color: '#00E396',
        }
      },
  },
]
})

const series = ref([])
const fanSeries = ref([])

onMounted(async () => {
  try {
    const resp = await api.get('/api/sensor/apex/?sensor=CPU_TEMP,GPU_TEMP,last=1h&resolution=1m')
    series.value = resp.data
    const resp2 = await api.get('/api/sensor/apex/?sensor=FAN_RPM,last=1h&resolution=1m')
    fanSeries.value = resp2.data
    const resp3 = await api.get('/api/switch/apex/')
    const _options: object = {
      fillColor: '#B3F7CA',
      opacity: 0.4,
      label: {
        borderColor: '#B3F7CA',
        style: {
          fontSize: '10px',
          color: '#fff',
          background: '#00E396',
        },
        offsetY: -10
      }
    }
    for (const item of resp3.data) {
      options.value.annotations?.xaxis?.push(merge(item, _options))
    }
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})


</script>

<template>
  <q-page class="row items-center justify-evenly full-width">
      <apexchart v-if="!loading" class="full-width" :height="CHART_HEIGHT" type="line" :options="options" :series="series"></apexchart>
      <apexchart v-if="!loading" class="full-width" :height="CHART_HEIGHT" type="line" :options="options" :series="fanSeries"></apexchart>
      <q-spinner-dots v-if="loading" size="5em"/>
  </q-page>
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
