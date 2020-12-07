from django.db import models
from accounts.models import CustomUser


class Point(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    beat_time = models.DateTimeField(auto_now_add=True)
