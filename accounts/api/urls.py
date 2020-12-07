from django.urls import path
from rest_framework.routers import SimpleRouter
from rest_framework.authtoken.views import obtain_auth_token

from .views import SignUpEmployeeViewSet


router = SimpleRouter()

urlpatterns = [
    path('signin/', obtain_auth_token),
    path('signup/', SignUpEmployeeViewSet.as_view()),
] + router.urls