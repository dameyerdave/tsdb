from django.core.management.base import BaseCommand
from friendlylog import colored_logger as log
from sys import stdin
import traceback
from core.models import Measurement
import re


class Command(BaseCommand):
    """
    Adds some mac metrics to the database.
    Please run:
    sudo powermetrics -s smc | docker exec -i tsdb-api-1 ./manage.py macmetrics
    """

    def add_arguments(self, parser):
        pass
        # parser.add_argument('action', type=str, help='The action to execute')
        # parser.add_argument('name', type=str, help='The name of the sensor or switch in question')
        # parser.add_argument('value', type=str, help='The value to add')
        # parser.add_argument('--timestamp-column', '-t', type=str, default=None, help='The timestamp field')

    def handle(self, *args, **options):
        try:
            for line in stdin:
                try:
                    if "CPU die temperature" in line:
                        value = float(
                            re.search(
                                r"CPU die temperature: ([-0-9\.]+) C", line
                            ).group(1)
                        )
                        Measurement.add("MAC", "CPU_TEMP", value)
                    if "GPU die temperature" in line:
                        value = float(
                            re.search(
                                r"GPU die temperature: ([-0-9\.]+) C", line
                            ).group(1)
                        )
                        Measurement.add("MAC", "GPU_TEMP", value)
                    if "Fan" in line:
                        value = float(re.search(r"Fan: ([0-9\.]+) rpm", line).group(1))
                        Measurement.add("MAC", "FAN_RPM", value)
                except Exception:
                    log.warning(f"Cannot parce: {line}.")
                    traceback.print_exc()
                    continue
        except Exception as ex:
            log.error(ex)
            traceback.print_exc()
