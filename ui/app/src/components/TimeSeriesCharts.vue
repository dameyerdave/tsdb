<script setup lang="ts">
import TimeSeriesChart from 'src/components/TimeSeriesChart.vue'
import {ref, onMounted} from 'vue'
import {api} from 'src/boot/axios'

const loading = ref(true)
const charts = ref()

onMounted(async () => {
    try {
        const resp = await api.get('/api/chart/')
        charts.value = resp.data.results
    } catch (err) {
        console.error(err)
    } finally {
        loading.value = false
    }
})
</script>

<template>
    <q-page class="row items-center justify-evenly full-width">
        <q-spinner-dots v-if="loading" size="5em" />
        <time-series-chart v-for="chart in charts" :key="chart.name" :chart="chart" />
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
