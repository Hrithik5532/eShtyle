from django.shortcuts import render

# Create your views here.

from rest_framework import generics
from .models import Portfolio
from .serializers import PortfolioSerializer

class PortfolioListView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.all().order_by('-likes', 'rank')    