from drf_auto_endpoint.router import register
from drf_auto_endpoint.endpoints import Endpoint
from .models import SensorReading, SwitchState
from .serializers import SensorReadingSerializer, SwitchStateSerializer
from .views import SensorReadingViewSet, SwitchStateViewSet


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
