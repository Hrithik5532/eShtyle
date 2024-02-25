from rest_framework import generics
from .models import SQP, AllProducts, Cart, wishlist
from .serializers import SQPSerializer, AllProductsSerializer, CartSerializer, WishlistSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Cart
from .serializers import CartSerializer


# AllProducts Views
class AllProductsListView(generics.ListAPIView):
    queryset = AllProducts.objects.all()
    serializer_class = AllProductsSerializer

class AllProductsDetailView(generics.RetrieveAPIView):
    queryset = AllProducts.objects.all()
    serializer_class = AllProductsSerializer

# SQP Views
class SQPListView(generics.ListAPIView):
    queryset = SQP.objects.all()
    serializer_class = SQPSerializer

class SQPDetailView(generics.RetrieveAPIView):
    queryset = SQP.objects.all()
    serializer_class = SQPSerializer




class AddToCartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # No change needed if user is handled via serializer's extra_kwargs
        # and portfolio is directly passed in the request body
        serializer.save(user=self.request.user)




# Wishlist Views
# Example: Add to Wishlist
class AddToWishlistView(generics.CreateAPIView):
    queryset = wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)