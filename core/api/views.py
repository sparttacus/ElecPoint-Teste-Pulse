from datetime import datetime

from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from accounts.models import CustomUser
from ..models import DayPoint, DayBeat
from .serializers import PointSerializer


class BeatsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(docid=request.POST["cpf"])
        except CustomUser.DoesNotExist:
            raise Response({"detail": "User with this DOC-ID was not found"}, status=404)

        try:
            day_point = DayPoint.objects.get(employee=user, date=datetime.now().today())
        except DayPoint.DoesNotExist:
            day_point = DayPoint.objects.create(employee=user, date=datetime.now().today())

        try:
            day_beat = DayBeat.objects.get(point=day_point)
        except DayBeat.DoesNotExist:
            day_beat = DayBeat.objects.create(point=day_point)

        if not day_beat.mark_two and not day_beat.mark_three and not day_beat.mark_four:
            day_beat.mark_two = datetime.now()
            day_beat.save()
        elif day_beat.mark_two and not day_beat.mark_three and not day_beat.mark_four:
            day_beat.mark_three = datetime.now()
            day_beat.save()
        elif day_beat.mark_two and day_beat.mark_three and not day_beat.mark_four:
            day_beat.mark_four = datetime.now()
            day_beat.save()

        serializer = PointSerializer(day_beat)
        return Response(serializer.data, status=201)

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(docid=request.GET["cpf"])
        except CustomUser.DoesNotExist:
            raise Response({"detail": "User with this DOC-ID was not found"}, status=404)

        if user != request.user:
            return Response({"detail": "You can see only your point beats"})

        date = request.GET.get("dia")

        if date:
            daily_point = DayPoint.objects.filter(employee=user, date=date).first()
        else:
            daily_point = DayPoint.objects.filter(employee=user, date=datetime.now().today()).first()

        if daily_point:
            daily_beats = DayBeat.objects.filter(point=daily_point).first()
            if daily_beats:
                serializer = PointSerializer(daily_beats)
                return Response(serializer.data, status=200)

        return Response({"detail": "beats not found"}, status=404)


class ListPeriodBeatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = CustomUser.objects.get(docid=request.GET["cpf"])
        except CustomUser.DoesNotExist:
            raise Response({"detail": "User with this DOC-ID was not found"}, status=404)

        if user != request.user:
            return Response({"detail": "You can see only your point beats"})

        _from = request.GET.get("de")
        to = request.GET.get("ate")

        if _from and to:
            daily_points = DayPoint.objects.filter(employee=user, date__range=(_from, to))
        else:
            daily_points = DayPoint.objects.filter(employee=user, date__month=datetime.now().month)

        data = {
            "total_worked_hours": 0,
            "total_extra_worked_hours": 0,
            "total_beats_count": 0,
        }
        for daily_point in daily_points:
            daily_beat = DayBeat.objects.fitler(point=daily_point).first()
            if daily_beat:
                beat_serializer = PointSerializer(daily_beat)
                data["total_worked_hours"] += beat_serializer.data["worked_hours"]
                data["total_extra_worked_hours"] += beat_serializer.data["extra_worked_hours"]
                data["total_beats_count"] += beat_serializer.data["beats_count"]

        return Response(data, status=200)


"""
- Consulta de ocorrências da empresa

    Eu como usuário do SPE desejo informar uma data de inicio e uma data de fim e ter como retorno o CPF de todos os usuários e a quantidade de ocorrências que cada um dos usuários cometeu nesse intervalo de tempo.
"""
class ListCompanyFaults(APIView):
    def get(self, request, *args, **kwargs):
        _from = request.GET.get("de")
        to = request.GET.get("ate")

        data = {}

        if _from and to:
            daily_points = DayPoint.objects.filter(date__range=(_from, to))
        else:
            daily_points = DayPoint.objects.filter(date__month=datetime.now().month)

        for day_point in daily_points:
            data[day_point.employee.docid] = 0

        for employee_cpf in data.keys():
            day

"""
- Consulta de ocorrências de um usuário

    Eu como usuário do SPE desejo informar um CPF, uma data de inicio, uma data de fim e ter como retorno todas as ocorrências do usuário ligado ao CPF informado e os pontos batidos nos dias das ocorrências.
"""
class ListEmployeeFaults(APIView):
    def get(self, request, *args, **kwargs):
        pass

