from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from ..models import CustomUser
from .serializers import EmployeeSerializer


class SignUpEmployeeViewSet(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        serializer = EmployeeSerializer(data=request.DATA)
        if serializer.is_valid():
            CustomUser.objects.create_user(
                "",
                serializer.init_data['username'],
                serializer.init_data['password']
            )

            return Response(serializer.data, status=201)
        else:
            return Response(serializer._errors, status=400)
