from django.urls import path
from .views import *


urlpatterns = [
    path('leaderboard', PortfolioListView.as_view(), name='leaderboard'),
    path('delete/image', delete_portfoilio),
    path('api/removebg', remove_bg),
    path('generate-image',generate_image),
    
    path('portfolio', PortfolioDetailView.as_view(), name='portfolio-detail'),
    path('images/eshtyle', ImagesEshtyle),

    
    path('blogs', BlogsListView.as_view(), name='blogs'),
    path('blog', BlogDetailView.as_view()),
    
    path('api/bookmark', book_mark_crud, name='bookmarks'),
    path('api/like', likes_crud, name='likes_crud'),
    
    path('api/vtryon',vtryon),
    path('api/portfolio_publish',portfolio_publish),
    
    path('api/generate-blog',generate_blog)
]