from django.db import models
from django.contrib.postgres.fields import ArrayField
from colorfield.fields import ColorField
from deepmerge import always_merger
from timescale.db.models.models import TimescaleModel
from django.utils.timezone import now

import json


def get_apex_options_schema():
    with open("core/schemas/apex_options.json", "r") as schema_file:
        return json.load(schema_file)


def get_default_apex_options():
    with open("core/schemas/apex_options_default.json", "r") as defaults_file:
        return json.load(defaults_file)


# class TimescaleModel(models.Model):
#     def save(self, *args, **kwargs):
#         # We want to smear the timestamp if sensors are read at the same time
#         # we just add a µs to the time
#         while self.__class__.objects.filter(time=self.time).exists():
#             self.time += td(microseconds=1)
#         super().save(*args, **kwargs)

#     class Meta:
#         abstract = True


class Entity(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Feature(models.Model):
    name = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class AnnotationDefinition(models.Model):
    COLORS = {"I": "#0f0", "W": "#FFA%00", "E": "#f00"}
    name = models.CharField(max_length=50, unique=True)
    level = models.CharField(
        max_length=1, choices=(("I", "INFO"), ("W", "WARN"), ("E", "ERROR"))
    )

    @property
    def color(self):
        return self.COLORS[self.level]

    def __str__(self):
        return self.name


class Measurement(TimescaleModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE)
    value = models.FloatField()

    @classmethod
    def add(cls, entity: str, feature: str, value: float):
        _entity, _ = Entity.objects.get_or_create(name=entity)
        _feature, _ = Feature.objects.get_or_create(name=feature)
        cls.objects.create(time=now(), entity=_entity, feature=_feature, value=value)

    def __str__(self):
        return f"[{self.time}] {self.entity.name} | {self.feature.name}: {self.value}"

    class Meta:
        ordering = ("time",)
        unique_together = ("time", "entity", "feature")
        index_together = [
            ("time", "entity", "feature"),
            ("entity", "feature"),
        ]


class Annotation(TimescaleModel):
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE)
    definition = models.ForeignKey(AnnotationDefinition, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.definition.name}"


# class SwitchState(TimescaleModel):
#     time = models.DateTimeField(default=timezone.now, primary_key=True)
#     switch = models.ForeignKey(Switch, on_delete=models.CASCADE)
#     on = models.BooleanField(default=False)

#     @classmethod
#     def add(cls, switch: str, on: bool):
#         _switch, created = Switch.objects.get_or_create(name=switch)
#         cls.objects.create(switch=_switch, on=on)

#     class Meta:
#         unique_together = ("time", "switch")
#         index_together = [
#             ("time", "switch"),
#         ]
#         ordering = ("time",)


class ApexConfig(models.Model):
    name = models.CharField(max_length=50, unique=True)
    inherit = models.ForeignKey(
        "ApexConfig",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="inheritors",
    )
    mixins = models.ManyToManyField(
        "ApexConfig", related_name="mixin_sources", blank=True
    )
    own_config = models.JSONField(
        default=get_default_apex_options, null=True, blank=True
    )

    @property
    def config(self):
        _config = {}
        if self.inherit:
            _config = always_merger.merge(_config, self.inherit.own_config)
        if self.mixins:
            for mixin in self.mixins.order_by("name"):
                _config = always_merger.merge(_config, mixin.own_config)
        if self.own_config:
            _config = always_merger.merge(_config, self.own_config)
        return _config

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("name",)


class ApexChart(models.Model):
    related_name = "charts"
    name = models.CharField(max_length=50, unique=True)
    xaxis_label = models.CharField(max_length=50, null=True, blank=True)
    yaxis_labels = ArrayField(
        models.CharField(max_length=50, null=True, blank=True), blank=True
    )
    group = models.CharField(max_length=50, null=True, blank=True)
    measurements = ArrayField(models.CharField(max_length=50, blank=True), blank=True)
    colors = ArrayField(ColorField(default="#000", blank=True), blank=True)
    tickAmount = models.IntegerField(default=6, blank=True)
    own_config = models.ForeignKey(
        ApexConfig, on_delete=models.RESTRICT, related_name=related_name
    )

    @property
    def config(self):
        _config = {
            "colors": self.colors,
            "stroke": {
                "curve": ["smooth"] * len(self.measurements),
                "width": [1] * len(self.measurements),
            },
        }
        if self.own_config:
            _config = always_merger.merge(_config, self.own_config.config)
        _config = always_merger.merge(
            _config, {"chart": {"id": f"chart{self.pk}"}, "title": {"text": self.name}}
        )
        if self.group:
            _config = always_merger.merge(_config, {"chart": {"group": self.group}})
        if self.xaxis_label:
            _config = always_merger.merge(
                _config,
                {
                    "xaxis": {
                        "title": {
                            "text": self.xaxis_label,
                            # "offsetX": -800,
                            "offsetY": 65,
                        }
                    }
                },
            )
        if self.yaxis_labels:
            _config = always_merger.merge(
                _config,
                {
                    "yaxis": [
                        {
                            "labels": {
                                "style": {
                                    "colors": [self.colors[idx]] * self.tickAmount
                                }
                            },
                            "axisTicks": {
                                "show": True,
                                "color": self.colors[idx],
                            },
                            "axisBorder": {"show": True, "color": self.colors[idx]},
                            "title": {
                                "text": measurement,
                                "style": {"color": self.colors[idx]},
                            },
                            "forceNiceScale": True,
                        }
                        for idx, measurement in enumerate(self.measurements)
                    ]
                },
            )
        return _config

    def __str__(self):
        return self.name

    class Meta:
        ordering = ("id",)
