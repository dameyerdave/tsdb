from django.test import TestCase, override_settings
from rest_framework.test import APIClient
from rest_framework import status
from .models import Entity, Feature, Measurement
import random
from django.utils.timezone import now
from datetime import timedelta as td


class Apex_Test(TestCase):
    def add_measurement_data(self):
        """Adds Entity / Feature data to test"""
        entity = "ENTITY"
        _entity, created = Entity.objects.get_or_create(name=entity)
        feature = "SENSOR"
        _feature, created = Feature.objects.get_or_create(name=feature)

        # One random value every minute for the last hour
        _now = now()
        _time = _now - td(hours=1)
        while _time < _now:
            value = random.uniform(0, 80)
            Measurement.objects.create(
                time=_time, entity=_entity, feature=_feature, value=value
            )
            _time = _time + td(minutes=1)

    def setUp(self):
        self.add_measurement_data()
        self.assertEqual(60, Measurement.objects.count())
        self.client = APIClient()

    @override_settings(APEX_DEFAULT_LAST="2h", APEX_DEFAULT_RESOLUTION="1m")
    def test_apex_sensor_data_retrieval(self):
        """Test the correctness of apex data retrieval"""
        response = self.client.get("/api/measurement/apex/?entity=ENTITY")
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual("SENSOR", data[0]["name"])
        self.assertEqual(60, len(data[0]["data"]))

    def test_apex_sensor_data_retrieval_with_parameters(self):
        """Test the correctness of apex data retrieval with parameters"""
        response = self.client.get(
            "/api/measurement/apex/?entity=ENTITY&last=2h&resolution=15m"
        )
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        data = response.json()
        self.assertEqual(1, len(data))
        self.assertEqual("SENSOR", data[0]["name"])
        self.assertEqual(5, len(data[0]["data"]))

    def test_add_measurement_data_at_same_time(self):
        _entity, created = Entity.objects.get_or_create(name="entity")
        _feature1, created = Feature.objects.get_or_create(name="sensor1")
        _feature2, created = Feature.objects.get_or_create(name="sensor2")

        _now = now()
        _time = _now - td(minutes=2)

        Measurement.objects.create(
            time=_time, entity=_entity, feature=_feature1, value=1.0
        )
        Measurement.objects.create(
            time=_time, entity=_entity, feature=_feature2, value=1.0
        )
