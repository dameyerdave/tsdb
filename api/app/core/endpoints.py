from drf_auto_endpoint.router import register
from drf_auto_endpoint.endpoints import Endpoint
from .models import Measurement, Feature, Entity, ApexConfig, ApexChart
from .serializers import (
    MeasurementSerializer,
    FeatureSerializer,
    EntitySerializer,
    ApexConfigSerializer,
    ApexChartSerializer,
)
from .views import (
    MeasurementViewSet,
    ApexConfigViewSet,
    ApexChartViewSet,
)


class DefaultEndpoint(Endpoint):
    """The default Endpoint"""

    include_str = False

    def get_url(self):
        """The core endpoint defaults to not include the application name in the apis url."""
        if hasattr(self, "url") and self.url is not None:
            return self.url

        return "{}".format(self.model_name.replace("_", "-"))


@register
class EntityEndpoint(DefaultEndpoint):
    url = "entity"
    model = Entity

    base_serializer = EntitySerializer

    filter_fields = ("name",)


@register
class FeatureEndpoint(DefaultEndpoint):
    url = "feature"
    model = Feature

    base_serializer = FeatureSerializer

    filter_fields = ("name",)


@register
class MeasurementEndpoint(DefaultEndpoint):
    url = "measurement"
    model = Measurement

    base_serializer = MeasurementSerializer
    base_viewset = MeasurementViewSet

    filter_fields = ("entity__name", "feature__name")


# @register
# class SwitchEndpoint(DefaultEndpoint):
#     url = "switch"
#     model = SwitchState

#     base_serializer = SwitchStateSerializer
#     base_viewset = SwitchStateViewSet

#     filter_fields = ("switch__name",)


@register
class ApexConfigEndpoint(DefaultEndpoint):
    url = "config"
    model = ApexConfig

    base_serializer = ApexConfigSerializer
    base_viewset = ApexConfigViewSet

    filter_fields = ("name",)


@register
class ApexChartEndpoint(DefaultEndpoint):
    url = "chart"
    model = ApexChart

    base_serializer = ApexChartSerializer
    base_viewset = ApexChartViewSet

    filter_fields = ("name",)
