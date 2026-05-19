from django.urls import path
from . import views

urlpatterns = [
    path('buy/', views.buy_lotto, name='buy'),
    path('history/', views.my_lotto_history, name='history'),
]