from rest_framework import serializers
from .models import SensorReading, SwitchState


class SensorReadingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorReading
        fields = '__all__'


class SwitchStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SwitchState
        fields = '__all__'
