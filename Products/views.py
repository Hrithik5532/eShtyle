from rest_framework import generics
from .models import SQP, AllProducts, Cart, wishlist
from .serializers import SQPSerializer, AllProductsSerializer, CartSerializer, WishlistSerializer

from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from .models import Cart
from .serializers import CartSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import api_view
from DesignGenerator.models import *
from DesignGenerator.serializers import *

@api_view(['GET'])
def all_products_list_view(request):
    if request.method == 'GET':
        serializer = AllProductsSerializer(AllProducts.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def product_detail(request,pk):
    if request.method == 'GET':
        portfolio = Portfolio.objects.get(id=pk)
        serializer = PortfolioSerializer(portfolio)
        data = serializer.data
        if  BookMark.objects.filter(portfolio=portfolio).exists():
            data['bookmarked'] = True
        else:
            data['bookmarked'] = False
        
        if Likes.objects.filter(portfolio=portfolio).exists():
            data['like'] = True
        else:
            data['like'] = False
        
        if Cart.objects.filter(portfolio=portfolio).exists():
            data['in_cart'] = True
        else:
            data['in_cart'] = False
        
        data['creator'] =portfolio.user.username
        return Response(data, status=status.HTTP_200_OK)

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


class MyCartView(generics.ListAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        This view should return a list of all the carts
        for the currently authenticated user.
        """
        user = self.request.user
        return Cart.objects.filter(user=user)


class UpdateCartView(generics.UpdateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Only allow updating carts belonging to the current user.
        """
        user = self.request.user
        return Cart.objects.filter(user=user)
    
    
    
class DeleteCartView(generics.DestroyAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Only allow deletion of carts belonging to the current user.
        """
        user = self.request.user
        return Cart.objects.filter(user=user)



class DeleteWishListView(generics.DestroyAPIView):
    queryset = wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        """
        Only allow deletion of carts belonging to the current user.
        """
        user = self.request.user
        return wishlist.objects.filter(user=user)


# Wishlist Views
# Example: Add to Wishlist
class AddToWishlistView(generics.CreateAPIView):
    queryset = wishlist.objects.all()
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        

class MyWishlistView(generics.ListAPIView):
    serializer_class = WishlistSerializer
    permission_classes = [IsAuthenticated]

    
    def get_queryset(self):
        """
        This view should return a list of all the carts
        for the currently authenticated user.
        """
        user = self.request.user
        return wishlist.objects.filter(user=user)