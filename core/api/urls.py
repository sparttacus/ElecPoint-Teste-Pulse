from django.urls import re_path
from rest_framework.routers import SimpleRouter

from . import views

router = SimpleRouter()
router.register(r'beats', views.BeatsViewSet)
router.register(r'beats/daily', views.ListDailyBeatsViewSet)

urlpatterns = [
    re_path(
        r'^company/(?P<company_id>[0-9])/events/$',
        views.ListCompanyEventsView.as_view(),
    ),
] + router.urls