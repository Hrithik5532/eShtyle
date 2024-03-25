from django.urls import path
from .views import *
from django.urls import path, re_path

urlpatterns = [
    path('products', all_products_list_view, name='all-products-list'),
    path('<int:pk>', product_detail, name='all-products-detail'),
    path('sqp', SQPListView.as_view(), name='sqp-list'),
    re_path(r'^sqp/(?P<pk>[0-9a-f-]+)/$', SQPDetailView.as_view(), name='sqp-detail'),
    path('add-to-cart', AddToCartView.as_view(), name='add-to-cart'),
    path('add-to-wishlist', AddToWishlistView.as_view(), name='add-to-wishlist'),
    
     path('my-cart', MyCartView.as_view(), ),
    path('my-wishlist', MyWishlistView.as_view(),),
    
     path('update-cart/<int:pk>', UpdateCartView.as_view(), name='update-cart'),
    path('delete-cart/<int:pk>', DeleteCartView.as_view(), name='delete-cart'),
   
       path('delete-wishlist/<int:pk>', DeleteWishListView.as_view(),),

]


