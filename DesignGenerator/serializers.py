from rest_framework import serializers
from .models import *
from Authentication.serializers import UserProfileUpdateSerializer

class TaggedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggableManager()
        fields = '__all__'


class PortfolioSerializer(serializers.ModelSerializer):
     # Assuming this is already defined elsewhere correctly
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Portfolio
        fields = '__all__'  # List all other fields explicitly if '__all__' is not desired

    def get_tags(self, obj):
        return [tag.name for tag in obj.tags.all()]

class CategoryBlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBlog
        fields = '__all__'

class Bolgserializer(serializers.ModelSerializer):
    category = CategoryBlogSerializer()
    class Meta:
        model = Blogs
        fields = '__all__'
        

class BookMarkSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer()
    class Meta:
        model = BookMark
        fields = '__all__'
    
class LikesSerializer(serializers.ModelSerializer):
    portfolio = PortfolioSerializer()
    class Meta:
        model = Likes
        fields = '__all__'
        
# class VirtualTryOnSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = VirtualTryOn
#         fields = '__all__'