from rest_framework import serializers
from .models import Measurement, Feature, Entity, ApexConfig, ApexChart


class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = "__all__"


class FeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feature
        fields = "__all__"


class EntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Entity
        fields = "__all__"


class ApexConfigSerializer(serializers.ModelSerializer):
    config = serializers.DictField()

    class Meta:
        model = ApexConfig
        fields = ("name", "config")


class ApexChartSerializer(serializers.ModelSerializer):
    config = serializers.DictField()

    class Meta:
        model = ApexChart
        fields = "__all__"
