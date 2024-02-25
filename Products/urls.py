from django.urls import path
from .views import (AllProductsListView, AllProductsDetailView, SQPListView, SQPDetailView,
                    AddToCartView, AddToWishlistView)
from django.urls import path, re_path

urlpatterns = [
    path('products/', AllProductsListView.as_view(), name='all-products-list'),
    path('<int:pk>/', AllProductsDetailView.as_view(), name='all-products-detail'),
    path('sqp/', SQPListView.as_view(), name='sqp-list'),
    re_path(r'^sqp/(?P<pk>[0-9a-f-]+)/$', SQPDetailView.as_view(), name='sqp-detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('add-to-wishlist/', AddToWishlistView.as_view(), name='add-to-wishlist'),
]
