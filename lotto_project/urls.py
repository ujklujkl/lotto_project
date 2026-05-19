# config/urls.py 또는 프로젝트명/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('lotto/', include('lotto.urls')),
]