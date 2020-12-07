from datetime import datetime

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from ..models import Point
from .serializers import PointSerializer


def count_beats(points):
    days = points.values('beat_time__day').distinct()


class BeatsViewSet(
    GenericViewSet,
    mixins.CreateModelMixin,
    mixins.ListModelMixin
):
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]
    queryset = Point.objects.all()

    def get_queryset(self):
        if self.action == "list":
            _from = self.request.GET["from"]
            _to = self.request.GET["to"]
            if _from and _to:
                return Point.objects.filter(
                    user__docid=self.request.GET["docid"],
                    beat_time__range=(_from, _to),
                )
            else:
                return Point.objects.filter(
                    user=self.request.user,
                    beat_time__month=datetime.now().month,
                )

        return Point.objects.filter(user=self.request.user)

    def list(self, request):
        data = {
            "worked_hours": 0,
            "extra_hours": 0,
            "beats_count": 0
        }

        points = self.get_queryset().order_by('beat_time')
        point_days = points.values_list('beat_time', flat=True).distinct()

        for day_dt in point_days:
            daily_points = points.filter(beat_time__date=day_dt).order_by('beat_time')
            if day_dt.weekday() != 5:
                if daily_points.count() == 1:
                    pass
                elif daily_points.count() == 2:
                    pass
                elif daily_points.count() == 3:
                    pass
                elif daily_points.count() == 4:
                    pass
                else:
                    pass
                for index in range(4):
                    daily_points[index]
            else:
                pass

        return Response(data)


class ListDailyBeatsViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = PointSerializer
    permission_classes = [IsAuthenticated]
    queryset = Point.objects.all()

    def get_queryset(self):
        _date = self.request.GET["date"]
        if _date:
            return Point.objects.filter(
                user=self.request.user,
                beat_time__day=_date,
            )
        return Point.objects.filter(
            user=self.request.user,
            beat_time__day=datetime.now().today(),
        )
    
    def list(self, request):
        pass


class ListCompanyEventsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        pass


class ListEmployeeEventsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        pass