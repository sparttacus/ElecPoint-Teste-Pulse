from datetime import datetime

from rest_framework import fields
from rest_framework.serializers import ModelSerializer

from .. import models



class PointSerializer(ModelSerializer):
    worked_hours = fields.SerializerMethodField()
    extra_worked_hours = fields.SerializerMethodField()
    beats_count = fields.SerializerMethodField()
    date = fields.DateField(source="point.date")

    class Meta:
        model = models.DayBeat
        fields = [
            "worked_hours",
            "extra_worked_hours", 
            "beats_count",
            "date",
            'mark_one',
            'mark_two',
            'mark_three',
            'mark_four',
        ]

    def get_worked_hours(self, obj):
        _worked_seconds = 0
        if obj.point.date.weekday() != 5: # Not saturnday
            if obj.mark_one and not obj.mark_two: # Debit
                return 0
            # Beat 1 | Beat 2
            if obj.mark_one.time() >= datetime.time(datetime(1,1,1,8,00))\
                    and obj.mark_two.time() > datetime.time(datetime(1,1,1,12,00)):
                _worked_seconds += (
                    datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            12,
                            00,
                        )
                    ) - obj.mark_one
                ).total_seconds()
            elif obj.mark_one.time() < datetime.time(datetime(1,1,1,8,00))\
                    and obj.mark_two.time() > datetime.time(datetime(1,1,1,12,00)):
                _worked_seconds += (
                    datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            12,
                            00,
                        )
                    ) - datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            8,
                            00,
                        )
                    )
                ).total_seconds()
            elif obj.mark_one.time() < datetime.time(datetime(1,1,1,8,00))\
                    and obj.mark_two.time() <= datetime.time(datetime(1,1,1,12,00)):
                _worked_seconds += (
                    obj.mark_two - datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            8,
                            00,
                        )
                    )
                ).total_seconds()
            else:
                _worked_seconds += (obj.mark_two - obj.mark_one).totalseconds()

            # Beat 3 | Beat 4
            if obj.mark_three and obj.mark_four:
                if obj.mark_three.time() >= datetime.time(datetime(1,1,1,14,00))\
                        and obj.mark_four.time() > datetime.time(datetime(1,1,1,18,00)):
                    _worked_seconds += (
                        datetime.time(
                            datetime(
                                obj.point.date.year,
                                obj.point.date.month,
                                obj.point.date.day,
                                18,
                                00,
                            )
                        ) - obj.mark_three
                    ).total_seconds()
                elif obj.mark_three.time() < datetime.time(datetime(1,1,1,14,00))\
                        and obj.mark_four.time() > datetime.time(datetime(1,1,1,18,00)):
                    _worked_seconds += (
                        datetime.time(
                            datetime(
                                obj.point.date.year,
                                obj.point.date.month,
                                obj.point.date.day,
                                18,
                                00,
                            )
                        ) - datetime.time(
                            datetime(
                                obj.point.date.year,
                                obj.point.date.month,
                                obj.point.date.day,
                                14,
                                00,
                            )
                        )
                    ).total_seconds()
                elif obj.mark_three.time() < datetime.time(datetime(1,1,1,14,00))\
                        and obj.mark_four.time() <= datetime.time(datetime(1,1,1,18,00)):
                    _worked_seconds += (
                        obj.mark_four - datetime.time(
                            datetime(
                                obj.point.date.year,
                                obj.point.date.month,
                                obj.point.date.day,
                                14,
                                00,
                            )
                        )
                    ).total_seconds()
                else:
                    _worked_seconds += (obj.mark_four - obj.mark_three).totalseconds()
        else:  # Saturnday
            if obj.mark_one and not obj.mark_two: # Debit
                return 0
            if obj.mark_one.time() >= datetime.time(datetime(1,1,1,8,00))\
                    and obj.mark_two.time() > datetime.time(datetime(1,1,1,12,00)):
                _worked_seconds += (
                    datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            12,
                            00,
                        )
                    ) - obj.mark_one
                ).total_seconds()
            elif obj.mark_one.time() < datetime.time(datetime(1,1,1,8,00))\
                    and obj.mark_two.time() > datetime.time(datetime(1,1,1,12,00)):
                _worked_seconds += (
                    datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            12,
                            00,
                        )
                    ) - datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            8,
                            00,
                        )
                    )
                ).total_seconds()
            elif obj.mark_one.time() < datetime.time(datetime(1,1,1,8,00))\
                    and obj.mark_two.time() <= datetime.time(datetime(1,1,1,12,00)):
                _worked_seconds += (
                    obj.mark_two - datetime.time(
                        datetime(
                            obj.point.date.year,
                            obj.point.date.month,
                            obj.point.date.day,
                            8,
                            00,
                        )
                    )
                ).total_seconds()
            else:
                _worked_seconds += (obj.mark_four - obj.mark_three).totalseconds()
            return _worked_seconds

    def get_extra_worked_hours(self, obj):
        _extra_seconds = 0
        if obj.mark_one:
            if obj.mark_one.time() < datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 8, 00)):
                _extra_seconds += (datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 8, 00)) - obj.mark_one).total_seconds()
        if obj.mark_two:
            if obj.mark_two.time() > datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 12, 00)):
                _extra_seconds += (datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 12, 00)) - obj.mark_one).total_seconds()
        if obj.mark_three:
            if obj.mark_three.time() < datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 14, 00)):
                _extra_seconds += (datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 14, 00)) - obj.mark_one).total_seconds()
        if obj.mark_four:
            if obj.mark_four.time() > datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 18, 00)):
                _extra_seconds += (datetime.time(datetime(obj.point.date.year, obj.point.date.month, obj.point.date.day, 18, 00)) - obj.mark_one).total_seconds()
        return _extra_seconds

    def debit_work_hours(self, obj):
        if self.worked_hours < obj.point.required_work_time:
            return obj.point.required_work_time - self.worked_hours
        return 0

    def get_beats_count(self, obj):
        _count = 1 if obj.mark_one else 0
        _count += 1 if obj.mark_two else 0
        _count += 1 if obj.mark_three else 0
        _count += 1 if obj.mark_four else 0
        return _count
