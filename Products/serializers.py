from rest_framework import serializers
from .models import SQP, AllProducts, Cart, wishlist

class SQPSerializer(serializers.ModelSerializer):
    class Meta:
        model = SQP
        fields = '__all__'

class AllProductsSerializer(serializers.ModelSerializer):
    sqp = SQPSerializer(many=True, read_only=True)

    class Meta:
        model = AllProducts
        fields = '__all__'

class CartSerializer(serializers.ModelSerializer):
    sqp = serializers.PrimaryKeyRelatedField(many=True, queryset=SQP.objects.all())

    class Meta:
        model = Cart
        fields = ['id', 'user', 'product', 'portfolio', 'quantity', 'sqp', 'created', 'updated']
        extra_kwargs = {'user': {'read_only': True}}

    def create(self, validated_data):
        sqp_data = validated_data.pop('sqp')
        cart = Cart.objects.create(**validated_data)
        cart.sqp.set(sqp_data)
        return cart

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = wishlist
        fields = '__all__'
