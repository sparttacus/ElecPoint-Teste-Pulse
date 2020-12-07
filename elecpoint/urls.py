from django.urls import path, include

from accounts.api import urls as accounts_urls
from core.api import urls as core_urls

urlpatterns = [
    path('accounts/', include(accounts_urls)),
    path('', include(core_urls)),
]
