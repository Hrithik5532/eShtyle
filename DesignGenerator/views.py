from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes,authentication_classes
from rest_framework.authentication import TokenAuthentication

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
# Create your views here.
from gradio_client import Client
import os
import random
from rest_framework import generics
from .models import *
from .serializers import *
from openai import OpenAI
    
from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings
import requests

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rembg import remove
from django.core.files.base import ContentFile
from io import BytesIO

from Authentication.views import  *


outfittryon = Client("https://levihsu-ootdiffusion.hf.space/")

texttoimage = Client("ByteDance/SDXL-Lightning")



class PortfolioListView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    queryset = Portfolio.objects.order_by('?').all()




@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def delete_portfoilio(request):
    if request.method == 'POST':
        user = request.user
        portfolio = get_object_or_404(Portfolio, pk=request.data.get('portfolio_id'))
        if portfolio.user == request.user:
            if portfolio.user == user:
                portfolio.delete()
                return Response({'message':'Deleted Successfully.'},status=status.HTTP_204_NO_CONTENT)
        else:
                return Response({'message':'Not allowed to Delete.'},status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def remove_bg(request):
    if request.method == 'POST':
        portfolio = get_object_or_404(Portfolio, id=request.data.get('portfolio_id'))
        if portfolio.user == request.user:
            image = portfolio.image

            # Convert the ImageField file to a byte stream
            image_bytes = image.file.read()

            # Use the byte stream with rembg's remove function
            result_bytes = remove(image_bytes)

            # Create a new image file from the result bytes
            result_image_file = ContentFile(result_bytes)
            new_image_name = 'processed_' + image.name

            # Create a new Portfolio instance
        
            # Copy other details from the original portfolio as needed
            # ...
            
            # Assign the new image to the image field and save
            portfolio.remove_bg.save(new_image_name, result_image_file)
            portfolio.save()

            # Return the URL of the new image

            return Response({'data': PortfolioSerializer(portfolio).data}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Not authorized to edit this portfolio.'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response({'message': 'Method not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
    
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def generate_image(request):
    if request.user.is_creator != True:
        return Response({'message':'You are not allowed to generate image.'},status=status.HTTP_401_UNAUTHORIZED)
    if request.method == 'POST':
        prompt = request.data.get('prompt')
        user = request.user
        try:
            suggestion = model.generate_content(f"Please check prompt is good for generating images to print on t-shirt or not. It should't be political, vulgar. Just give True if prompt is safe or False in response :{prompt} ")
            if suggestion.text == 'False':
                return Response({'message':'Please do not enter vulgar or conflict creating prompts.'},status=status.HTTP_400_BAD_REQUEST)

                
        except:
            return Response({'message':'Please do not enter vulgar or conflict creating prompts.'},status=status.HTTP_400_BAD_REQUEST)
        response = model.generate_content(f" give list of tags which are most important for search in ',' seperated from  The prompt:{prompt} ")
        steps = ['1-Step', '2-Step', '4-Step', '8-Step']
        
        
        result = texttoimage.predict(
                prompt, # str in 'Enter your prompt (English)' Textbox component
                random.choice(steps), # Literal['1-Step', '2-Step', '4-Step', '8-Step'] in 'Select inference steps' Dropdown component
                api_name="/generate_image"
        )

        # Extract the file path from the result
        file_path = result

        # Read the file content
        with open(file_path, 'rb') as file:
            content = file.read()

        # Create a new Portfolio instance
        title = model.generate_content(f"Please suggest one title for this  prompt. It should be related and meaningful to prompt :{prompt} ")

        portfolio = Portfolio(user=user)
        portfolio.title = title.text
        portfolio.description = prompt
        # It's important to save the portfolio before setting tags to ensure it has a primary key
        portfolio.image.save(os.path.basename(file_path), ContentFile(content), save=True)
        portfolio.save()  # Save the portfolio to assign a primary key before adding tags

        # Now that the portfolio has been saved, we can set the tags
        tag_names = response.text.split(',')
        tag_names = [tag.strip() for tag in tag_names if tag.strip()]

        portfolio.tags.add(*tag_names)  # This correctly associates the tags with the portfolio instance


        # Prepare the image URL for response
        try:
            os.remove(file_path)
            print(f"Successfully deleted file: {file_path}")
        except OSError as e:
            print(f"Error deleting file: {file_path}. Reason: {e.strerror}")
        return Response({'data': PortfolioSerializer(portfolio).data}, status=status.HTTP_200_OK)
    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def portfolio_publish(request):
    portfolio_id = request.POST.get('portfolio_id')
    portfolio = get_object_or_404(Portfolio, id=portfolio_id)
    if  portfolio.publish == True:
        portfolio.publish = False
        portfolio.save()
        return Response({'data': PortfolioSerializer(portfolio).data,'message':"Image not Published"}, status=status.HTTP_200_OK)

    else:
        portfolio.publish = True
        portfolio.save()

    
        return Response({'data': PortfolioSerializer(portfolio).data,'message':"Image is Published"}, status=status.HTTP_200_OK)
    
    
    
class PortfolioDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user  # Get the user making the request
        portfolio = Portfolio.objects.filter(user=user) # Retrieve user's portfolio or 404 if not found
        serializer = PortfolioSerializer(portfolio,many=True)  # Serialize portfolio data
        data = serializer.data
        for index, portfolio_data in enumerate(data):
            portfolio_instance = portfolio[index]
            if BookMark.objects.filter(portfolio=portfolio_instance).exists():
                data[index]['book_marked'] = True
            else:
                data[index]['book_marked'] = False
            
        for index, portfolio_data in enumerate(data):
            portfolio_instance = portfolio[index]
            if Likes.objects.filter(portfolio=portfolio_instance).exists():
                data[index]['likes'] = True
            else:
                data[index]['likes'] = False
            
            data[index]['likes_count'] = Likes.objects.filter(portfolio=portfolio_instance).count()
        return Response({'data':data},status=status.HTTP_200_OK)  # Return serialized data



class BlogsListView(generics.ListAPIView):
    serializer_class = Bolgserializer
    queryset = Blogs.objects.all().order_by('-id')


class BlogDetailView(generics.RetrieveAPIView):
    queryset = Blogs.objects.all()
    serializer_class = Bolgserializer




@api_view(['GET'])
def ImagesEshtyle(request):
    images = Portfolio.objects.filter(user__email='bqwenzen@gmail.com').order_by('?')
    serialized_images = PortfolioSerializer(images, many=True)
    
    data = serialized_images.data
    if request.user.is_authenticated:
        for index, portfolio_data in enumerate(data):
            portfolio_instance = images[index]
            data[index]['book_marked'] = BookMark.objects.filter(portfolio=portfolio_instance, user=request.user).exists()
            data[index]['likes'] = Likes.objects.filter(portfolio=portfolio_instance, user=request.user).exists()
            data[index]['likes_count'] = Likes.objects.filter(portfolio=portfolio_instance).count()

    return Response({'data': data}, status=status.HTTP_200_OK)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def book_mark_crud(request):
    if request.method == 'POST':
        user = request.user
        portfolio = Portfolio.objects.get(id=request.data.get('portfolio_id'))
        
        if BookMark.objects.filter(user=user, portfolio=portfolio).exists():
            BookMark.objects.get(user=user, portfolio=portfolio).delete()
            return Response({'message': 'Removed from BookMark'}, status=status.HTTP_200_OK)
        else:
            
            like = BookMark(user=user, portfolio=portfolio)
            like.save()
        
            return Response({'message': 'Addred to BookMark'}, status=status.HTTP_200_OK)
    
    if request.method == 'GET':
        user = request.user
        if BookMark.objects.filter(user=user).exists():
            bookmark = BookMark.objects.filter(user=user)
            return Response({'data': BookMarkSerializer(bookmark,many=True).data}, status=status.HTTP_200_OK)
       
    
    
    
    
@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def likes_crud(request):
    if request.method == 'POST':
        user = request.user
        portfolio = Portfolio.objects.get(id=request.data.get('portfolio_id'))
        if Likes.objects.filter(user=user, portfolio=portfolio).exists():
            Likes.objects.get(user=user, portfolio=portfolio).delete()
            return Response({'message': 'Unliked'}, status=status.HTTP_200_OK)
        else:
            like = Likes(user=user, portfolio=portfolio)
            like.save()
            return Response({'message': 'Liked'}, status=status.HTTP_200_OK)
    
    
from gradio_client import Client,file
import httpx

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def vtryon(request):
    if request.method == 'POST':
        cloth_image = request.FILES.get('cloth')
        model_image = request.FILES.get('model_image')
        if model_image:
            user = User.objects.get(id=request.user.id)
            user.full_body_image =model_image
            user.save()
        vton = VirtuallyTried.objects.create(user= request.user, cloth_image=cloth_image)
        vton.save()
        

        print(vton.user.full_body_image.url)
        model_image_path = '/home/eshtyle/eShtyle/media/'+str(vton.user.full_body_image)
        cloth_path = '/home/eshtyle/eShtyle/media/'+str(vton.cloth_image)
        
        print(model_image_path)
        print(cloth_path)
        result = outfittryon.predict(
            file(model_image_path),
            file(cloth_path),
            "Upper-body",
            1,
            20,
            2,
            -1,
            api_name="/process_dc",
        )
        print(result)
        
        file_path = result[0]['image']

        # Read the file content
        with open(file_path, 'rb') as file_:
            content = file_.read()

        # Create a new Portfolio instance

        # It's important to save the portfolio before setting tags to ensure it has a primary key
        vton.output_image.save(os.path.basename(file_path), ContentFile(content), save=True)
        vton.save()  # Save the portfolio to assign a primary key before adding tags
        try:
            os.remove(file_path)
            print(f"Successfully deleted file: {file_path}")
        except OSError as e:
            print(f"Error deleting file: {file_path}. Reason: {e.strerror}")
        # Now that the portfolio has been saved, we can set the tags
        
        return Response({'message': 'Files have been saved.','data':VirtuallyTriedSerializer(vton).data},status = status.HTTP_200_OK)

    return Response({'message': 'GET request received.'},status=status.HTTP_200_OK)
    
    
    
   
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([TokenAuthentication])
def generate_blog(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = model.generate_content(f"I want to create a blog on given title. Give me Content in form of RichTextField as i'm using CKeditor. Content should contain minimum to 300 words title = {title} ")
        return Response({'message': 'Blog Generated','data':content.text},status = status.HTTP_200_OK)