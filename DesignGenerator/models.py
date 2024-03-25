
#DesignGenerator/models.py
from django.db import models
from Authentication.models import User
# Create your models here.
from django.utils.deconstruct import deconstructible
from ckeditor.fields import RichTextField
from  taggit.managers import TaggableManager
@deconstructible
class PathAndRename(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'portfolio_images/{instance.user.id}/{filename}'
    
@deconstructible
class VtronPath(object):
    def __init__(self, sub_path):
        self.sub_path = sub_path

    def __call__(self, instance, filename):
        # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
        return f'vtry/{instance.user.id}/{filename}'


class Portfolio(models.Model):
    user  = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    tags = TaggableManager()
    image = models.ImageField(upload_to=PathAndRename("user"))
    remove_bg = models.ImageField(upload_to=PathAndRename("user"),blank=True, null=True)
    rank = models.IntegerField(default=0)
    used_by = models.IntegerField(default=0)
    
    publish = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    


class CategoryBlog(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class BlogTags(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Blogs(models.Model):

    title = models.CharField(max_length=255)
    category = models.ForeignKey(CategoryBlog, on_delete=models.CASCADE)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images/')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(BlogTags, blank=True)  # Removed null=True
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)




class BookMark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# class VirtualTryOn(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     model_image = models.ImageField(upload_to=VtronPath("user"))
#     cloth = models.ImageField(upload_to=VtronPath("user"))
#     vimage = models.ImageField(upload_to=VtronPath("user"),blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)












