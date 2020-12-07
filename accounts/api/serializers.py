from rest_framework import serializers

from ..models import CustomUser


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'first_name',
            'last_name',
            'docid',
            'email',
            'password',
            'photo_url',
        ]
