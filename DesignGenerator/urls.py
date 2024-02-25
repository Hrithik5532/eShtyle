from django.urls import path
from .views import *


urlpatterns = [
    path('leaderboard', PortfolioListView.as_view(), name='leaderboard'),
]