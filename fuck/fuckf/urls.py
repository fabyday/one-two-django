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
        
        
        # Post create list
        path('post/create', views.CreatePost.as_view()),


        # post delete get put update
        path('post/<str:test>/<int:pk>', views.PostDetail.as_view()),
        
        
        
        
        # path(, views.PostList.as_view()),
        path('post/<int:pk>/list', views.PostCategoryList.as_view()),

        path('post/category-list', views.PostCategoryList.as_view()),
        path('post/category/create', views.PostCategoryCreate.as_view()),
        # for debugging 
        # path('talk', views.TokenList.as_view()),
    ]



