from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import SensorReading, SwitchState, ApexConfig, ApexChart
from .serializers import SensorReadingSerializer, SwitchStateSerializer, ApexConfigSerializer, ApexChartSerializer
from .helpers import milliseconds, dictfetchall, value_unit, quote
from datetime import timedelta as td
from django.utils.timezone import now
from django.db import connection
from django.conf import settings


class SensorReadingViewSet(viewsets.ModelViewSet):
    queryset = SensorReading.objects.all()
    serializer_class = SensorReadingSerializer

    @action(detail=False, methods=['get'])
    def apex(self, request):
        """ Returns the data in apex chart format """
        sensor = request.GET.get('sensor')
        last_value, last_unit = value_unit(request.GET.get('last'), settings.APEX_DEFAULT_LAST)
        resolution_value, resolution_unit = value_unit(request.GET.get('resolution'), settings.APEX_DEFAULT_RESOLUTION)
        digits = request.GET.get('digits', settings.APEX_DEFAULT_DIGITS)
        sensor_filter = ''
        if sensor:
            sensor_filter = f"AND s.name IN ({','.join([quote(s) for s in sensor.split(',')])})"
        ret = {}
        with connection.cursor() as cursor:

            cursor.execute('''
                SELECT 
                    s.name AS sensor, 
                    time_bucket('{} {}', sr.time) AS timestamp, 
                    round(avg(sr.value)::numeric, {}) AS avg
                FROM core_sensorreading as sr
                INNER JOIN core_sensor s on sr.sensor_id = s.id 
                WHERE sr.time > '{}' {}
                GROUP BY s.name, timestamp
                ORDER BY timestamp
            '''.format(resolution_value, resolution_unit, digits, now() - td(**{last_unit: last_value}), sensor_filter))
            for dp in dictfetchall(cursor):
                if dp.sensor not in ret:
                    ret[dp.sensor] = {'name': dp.sensor, 'data': []}
                ret[dp.sensor]['data'].append({'x': milliseconds(dp.timestamp), 'y': dp.avg})

        return Response([r for r in ret.values()], status.HTTP_200_OK)


class SwitchStateViewSet(viewsets.ModelViewSet):
    queryset = SwitchState.objects.all()
    serializer_class = SwitchStateSerializer

    @action(detail=False, methods=['get'])
    def apex(self, request):
        """ Returns the data in apex chart format """
        switch = request.GET.get('switch')
        last_value, last_unit = value_unit(request.GET.get('last'), settings.APEX_DEFAULT_LAST)
        resolution_value, resolution_unit = value_unit(request.GET.get('resolution'), settings.APEX_DEFAULT_RESOLUTION)
        switch_filter = ''
        if switch:
            switch_filter = f"AND s.name IN ({switch})'"
        ret = {}
        with connection.cursor() as cursor:
            cursor.execute('''
                SELECT 
                    s.name AS switch, 
                    time_bucket('{} {}', sr.time) AS timestamp, 
                    bool_or(sr.on) AS on
                FROM core_switchstate as sr
                INNER JOIN core_switch s on sr.switch_id = s.id 
                WHERE sr.time > '{}' {}
                GROUP BY s.name, timestamp
                ORDER BY timestamp
            '''.format(resolution_value, resolution_unit, now() - td(**{last_unit: last_value}), switch_filter))
            cnt = 0
            for dp in dictfetchall(cursor):
                key = f"{dp.switch}_{cnt}"
                if key not in ret:
                    ret[key] = {'label': {'text': dp.switch}}
                if dp.on:
                    ret[key]['x'] = milliseconds(dp.timestamp)
                elif 'x' in ret[key]:
                    ret[key]['x2'] = milliseconds(dp.timestamp)
                    cnt += 1
            # If the last switch state is on we set the x2 to current time
            if len(ret) > 0:
                if 'x2' not in ret[key]:
                    ret[key]['x2'] = milliseconds(now())

        return Response([r for r in ret.values()], status.HTTP_200_OK)


class ApexConfigViewSet(viewsets.ModelViewSet):
    queryset = ApexConfig.objects.all()
    serializer_class = ApexConfigSerializer
    filterset_fields = ('name',)


class ApexChartViewSet(viewsets.ModelViewSet):
    queryset = ApexChart.objects.all()
    serializer_class = ApexChartSerializer
    filterset_fields = ('name',)
