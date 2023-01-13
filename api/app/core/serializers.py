from rest_framework import serializers
from .models import SensorReading, SwitchState, ApexConfig, ApexChart


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'


class SwitchStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchState
        fields = '__all__'


class ApexConfigSerializer(serializers.ModelSerializer):
    config = serializers.DictField()

    class Meta:
        model = ApexConfig
        fields = ('name', 'config')


class ApexChartSerializer(serializers.ModelSerializer):
    config = serializers.DictField()

    class Meta:
        model = ApexChart
        fields = '__all__'
