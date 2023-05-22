from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import APIException
from .models import ApexConfig, ApexChart, Measurement, Annotation
from .serializers import (
    MeasurementSerializer,
    ApexConfigSerializer,
    ApexChartSerializer,
)
from .helpers import milliseconds, value_unit, quote, dictfetchall
from datetime import timedelta as td
from django.utils.timezone import now

# from django.db.models import Avg
# from django.db.models.functions import Round
# from django.contrib.postgres.aggregates import StringAgg
from django.conf import settings
from django.db import connection


class MeasurementViewSet(viewsets.ModelViewSet):
    queryset = Measurement.timescale.all()
    serializer_class = MeasurementSerializer

    @action(detail=False, methods=["get"])
    def apex(self, request):
        """Returns the data in apex chart format"""
        entity = request.GET.get("entity")
        if not entity:
            raise APIException(
                "Parameter 'entity' is required.", status.HTTP_400_BAD_REQUEST
            )
        feature = request.GET.get("feature")
        last_value, last_unit = value_unit(
            request.GET.get("last"), settings.APEX_DEFAULT_LAST
        )
        resolution_value, resolution_unit = value_unit(
            request.GET.get("resolution"), settings.APEX_DEFAULT_RESOLUTION
        )
        digits = request.GET.get("digits", settings.APEX_DEFAULT_DIGITS)
        feature_filter = ""
        if feature:
            feature_filter = (
                f"AND f.name IN ({','.join([quote(s) for s in feature.split(',')])})"
            )
        # ranges = (now() - td(**{last_unit: last_value}), now())
        # measurements = self.queryset.filter(entity__name=entity)
        # if feature:
        #     features = feature.split(",")
        #     measurements = measurements.filter(feature__name__in=features)
        # measurements = (
        #     measurements.filter(time__range=ranges)
        #     .values("feature__name")
        #     .time_bucket("time", f"{resolution_value} {resolution_unit}")
        #     .annotate(
        #         feature=StringAgg("feature__name", ",", distinct=True),
        #         value=Round(Avg("value"), digits),
        #     )
        # )

        ret = {}
        # for measurement in measurements:
        #     if measurement["feature"] not in ret:
        #         ret[measurement["feature"]] = {
        #             "name": measurement["feature"],
        #             "data": [],
        #         }
        #     ret[measurement["feature"]]["data"].append(
        #         {"x": milliseconds(measurement["bucket"]), "y": measurement["value"]}
        #     )

        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    f.name AS feature,
                    time_bucket('{} {}', m.time) AS timestamp,
                    round(avg(m.value)::numeric, {}) AS avg
                FROM core_measurement as m
                INNER JOIN core_entity e on m.entity_id = e.id
                INNER JOIN core_feature f on m.feature_id = f.id
                WHERE e.name='{}' AND m.time > '{}' {}
                GROUP BY f.name, timestamp
                ORDER BY timestamp
            """.format(
                    resolution_value,
                    resolution_unit,
                    digits,
                    entity,
                    now() - td(**{last_unit: last_value}),
                    feature_filter,
                )
            )
            for dp in dictfetchall(cursor):
                if dp.feature not in ret:
                    ret[dp.feature] = {"name": dp.feature, "data": []}
                ret[dp.feature]["data"].append(
                    {"x": milliseconds(dp.timestamp), "y": dp.avg}
                )
        annotations = Annotation.objects.filter(entity__name=entity)

        return Response(
            {
                "series": [ret[f] for f in feature.split(",")],
                "annotations": [
                    {
                        "x": milliseconds(a.time),
                        "strokeDashArray": 0,
                        "borderColor": a.definition.color,
                        "label": {
                            "borderColor": a.definition.color,
                            "style": {
                                "color": "#000",
                                "background": a.definition.color,
                            },
                            "text": a.definition.name,
                        },
                    }
                    for a in annotations
                ],
            },
            status.HTTP_200_OK,
        )


# class SwitchStateViewSet(viewsets.ModelViewSet):
#     queryset = SwitchState.objects.all()
#     serializer_class = SwitchStateSerializer

#     @action(detail=False, methods=["get"])
#     def apex(self, request):
#         """Returns the data in apex chart format"""
#         switch = request.GET.get("switch")
#         last_value, last_unit = value_unit(
#             request.GET.get("last"), settings.APEX_DEFAULT_LAST
#         )
#         resolution_value, resolution_unit = value_unit(
#             request.GET.get("resolution"), settings.APEX_DEFAULT_RESOLUTION
#         )
#         switch_filter = ""
#         if switch:
#             switch_filter = f"AND s.name IN ({switch})'"
#         ret = {}
#         with connection.cursor() as cursor:
#             cursor.execute(
#                 """
#                 SELECT
#                     s.name AS switch,
#                     time_bucket('{} {}', sr.time) AS timestamp,
#                     bool_or(sr.on) AS on
#                 FROM core_switchstate as sr
#                 INNER JOIN core_switch s on sr.switch_id = s.id
#                 WHERE sr.time > '{}' {}
#                 GROUP BY s.name, timestamp
#                 ORDER BY timestamp
#             """.format(
#                     resolution_value,
#                     resolution_unit,
#                     now() - td(**{last_unit: last_value}),
#                     switch_filter,
#                 )
#             )
#             cnt = 0
#             for dp in dictfetchall(cursor):
#                 key = f"{dp.switch}_{cnt}"
#                 if key not in ret:
#                     ret[key] = {"label": {"text": dp.switch}}
#                 if dp.on:
#                     ret[key]["x"] = milliseconds(dp.timestamp)
#                 elif "x" in ret[key]:
#                     ret[key]["x2"] = milliseconds(dp.timestamp)
#                     cnt += 1
#             # If the last switch state is on we set the x2 to current time
#             if len(ret) > 0:
#                 if "x2" not in ret[key]:
#                     ret[key]["x2"] = milliseconds(now())

#         return Response([r for r in ret.values()], status.HTTP_200_OK)


class ApexConfigViewSet(viewsets.ModelViewSet):
    queryset = ApexConfig.objects.all()
    serializer_class = ApexConfigSerializer
    filterset_fields = ("name",)


class ApexChartViewSet(viewsets.ModelViewSet):
    queryset = ApexChart.objects.all()
    serializer_class = ApexChartSerializer
    filterset_fields = ("name",)
