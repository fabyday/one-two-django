from django.urls import include, path
from rest_framework import routers
from fuckf import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'board', views.BoardViewSet)


urlpatterns = [
        # path('', include(router.urls)),
        # path('what-ever/', include('rest_framework.urls', namespace='rest_framework'))
        path('users/', views.UserList.as_view()),
        path('users/signup/', views.RegisterView.as_view(), name='auth_register'),
        # path('login')
        path('users/<int:pk>/', views.UserDetail.as_view()),
        path('post/create', views.BoardCreateViewSet.as_view()),
        path('post/<int:pk>', views.BoardViewSet.as_view()),
    ]



