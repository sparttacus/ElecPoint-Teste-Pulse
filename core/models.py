from django.db import models
from django.utils import timezone

from accounts.models import CustomUser


class DayPoint(models.Model):
    employee = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    date = models.DateField(default=timezone.now)

    @property
    def required_work_hours(self):
        if self.date.weekday() == 5:
            return 4
        return 8

class DayBeat(models.Model):
    point = models.ForeignKey(DayPoint, on_delete=models.PROTECT)
    mark_one = models.DateTimeField(default=timezone.now)
    mark_two = models.DateTimeField(null=True)
    mark_three = models.DateTimeField(null=True)
    mark_four = models.DateTimeField(null=True)

    @property
    def beats_count(self):
        _count = 1 if self.mark_one else 0
        _count += 1 if self.mark_two else 0
        _count += 1 if self.mark_three else 0
        _count += 1 if self.mark_four else 0
        return _count
