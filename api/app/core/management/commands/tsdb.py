from django.core.management.base import BaseCommand
from django.utils import timezone
from friendlylog import colored_logger as log
from core.models import Sensor, SensorReading, Switch, SwitchState
from core.helpers import num_lines
from datetime import datetime as dt
from os.path import isfile
from tqdm import tqdm
import traceback
import csv


class TSDBError(Exception):
    pass


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='The action to execute')
        parser.add_argument('name', type=str, help='The name of the sensor or switch in question')
        parser.add_argument('value', type=str, help='The value to add')
        parser.add_argument('--timestamp-column', '-t', type=str, default=None, help='The timestamp field')

    def sensor_add(self, sensor: str, value: float, timestamp: str = None):
        SensorReading.add(sensor, value)
        log.debug(f"Added {value} to sensor '{sensor}'.")

    def switch_add(self, switch: str, on: bool):
        SwitchState.add(switch, on)
        log.debug(f"Set switch '{switch}' on to {on}.")

    def sensor_csv(self, filename: str, timestamp_column: str):
        if isfile(filename):
            with open(filename, 'r') as f:
                reader = csv.DictReader(f)
                for row in tqdm(reader, total=num_lines(filename)):
                    if not timestamp_column in row:
                        log.error(f"Timestamp column '{timestamp_column}' not found in '{filename}'.")
                        return
                    timestamp = None
                    for sensor, value in row.items():
                        if sensor == timestamp_column:
                            timestamp = dt.fromtimestamp(int(value), tz=timezone.utc)
                        else:
                            _sensor, created = Sensor.objects.get_or_create(name=sensor)
                            SensorReading.objects.create(time=timestamp, sensor=_sensor, value=float(value))
        else:
            log.error(f"Cannot find '{filename}'.")

    def parseBool(self, value):
        return value == 'true' \
            or value == 'True' \
            or value == 't' \
            or value == 'T' \
            or value == '1'

    def handle(self, *args, **options):
        try:
            if options.get('action') == 'sensor':
                self.sensor_add(options.get('name'), options.get('value'))
            elif options.get('action') == 'switch':
                self.switch_add(options.get('name'), self.parseBool(options.get('value')))
            elif options.get('action') == 'csv' and options.get('name') == 'sensor':
                self.sensor_csv(options.get('value'), options.get('timestamp_column'))
            elif options.get('action') == 'csv' and options.get('name') == 'switch':
                self.switch_csv(options.get('value'), options.get('timestamp_column'))
        except Exception as ex:
            log.error(ex)
            traceback.print_exc()
