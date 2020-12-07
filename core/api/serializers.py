from rest_framework.serializers import ModelSerializer

from .. import models


class PointSerializer(ModelSerializer):
    class Meta:
        model = models.Point
        fields = ['employee', 'beat_time']