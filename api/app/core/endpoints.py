from drf_auto_endpoint.router import register
from drf_auto_endpoint.endpoints import Endpoint
from .models import SensorReading, SwitchState, ApexConfig, ApexChart
from .serializers import SensorReadingSerializer, SwitchStateSerializer, ApexConfigSerializer, ApexChartSerializer
from .views import SensorReadingViewSet, SwitchStateViewSet, ApexConfigViewSet, ApexChartViewSet


class DefaultEndpoint(Endpoint):
    """The default Endpoint"""
    include_str = False

    def get_url(self):
        """ The core endpoint defaults to not include the application name in the apis url. """
        if hasattr(self, 'url') and self.url is not None:
            return self.url

        return '{}'.format(self.model_name.replace('_', '-'))


@register
class SensorEndpoint(DefaultEndpoint):
    url = 'sensor'
    model = SensorReading

    base_serializer = SensorReadingSerializer
    base_viewset = SensorReadingViewSet

    filter_fields = ('sensor__name',)


@register
class SwitchEndpoint(DefaultEndpoint):
    url = 'switch'
    model = SwitchState

    base_serializer = SwitchStateSerializer
    base_viewset = SwitchStateViewSet

    filter_fields = ('switch__name',)


@register
class ApexConfigEndpoint(DefaultEndpoint):
    url = 'config'
    model = ApexConfig

    base_serializer = ApexConfigSerializer
    base_viewset = ApexConfigViewSet

    filter_fields = ('name', )


@register
class ApexChartEndpoint(DefaultEndpoint):
    url = 'chart'
    model = ApexChart

    base_serializer = ApexChartSerializer
    base_viewset = ApexChartViewSet

    filter_fields = ('name', )
