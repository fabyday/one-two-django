from telnetlib import STATUS
from django.contrib.auth.models import User, Group
from rest_framework import permissions, response, status, viewsets
from .serializer import PostSerializer
from fuckf.serializer import UserSerializer, GroupSerializer
from fuckf.serializer import *
from rest_framework.authtoken.models import Token 
from fuckf.models import *
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication

##
## AUTHENTICATION
##
class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegisterSerializer

class LoginView(generics.GenericAPIView):
    """
        STATUS
        200 : successfully get Token
        400 : rejected create token
    """
    def post(self, request):
        user = authenticate(username = request.data['username'], password = request.data['password'])
        if user:
            token, created = Token.objects.get_or_create(user = user)
            return Response({'token' : token.key})
        return Response(None, status=status.HTTP_401_UNAUTHORIZED)

from rest_framework.authtoken.serializers import AuthTokenSerializer

class TokenList(generics.ListAPIView):
    queryset = Token.objects.all() 
    serializer_class = AuthTokenSerializer 

#####
# POST
#####

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)

class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        print("test req", request.data)
        print("test req", request.user)
        serializer = PostCreateSerializer(data= request.data)
        if serializer.is_valid():
            post = Post.objects.create(title = request.data['title'], author = request.user, contents = request.data['contents'])
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [Token]

