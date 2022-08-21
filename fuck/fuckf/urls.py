from django.urls import include, path
from rest_framework import routers
from fuckf import views


urlpatterns = [
        
        # user list(sign up)
        path('users/', views.UserList.as_view()),
        path('users/signup/', views.RegisterView.as_view()),
        path('users/<int:pk>/', views.UserDetail.as_view()),
        
        # auth(Token based)
        path('get-token', views.LoginView.as_view()),
        
        
        # Post CRUD 
        path('post/create', views.CreatePost.as_view()),
        path('post/list', views.PostList.as_view()),
        path('post/<int:pk>', views.PostDetail.as_view()),
        

        # for debugging 
        # path('talk', views.TokenList.as_view()),
    ]



