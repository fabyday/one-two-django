from telnetlib import STATUS
from tkinter import Image
from django.contrib.auth.models import User, Group
from rest_framework import permissions, response, status, viewsets
from .serializer import PostSerializer
from fuckf.serializer import UserSerializer
from fuckf.serializer import *
from rest_framework.authtoken.models import Token 
from fuckf.models import *
from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication, BasicAuthentication
from .custom_permission import *

class CategoryVisiblePermssion(permissions.BasePermission):
    """Allow users to update their own manuscripts libraries."""
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.manuscript.author == request.user

    def has_permission(self, request, view):
        authenticator = request._authenticator

        if request.method == 'POST':
            return True
        
        if request.method == "GET":
            return True
        

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

# from rest_framework.authtoken.serializers import AuthTokenSerializer

# class TokenList(generics.ListAPIView):
#     queryset = Token.objects.all() 
#     serializer_class = AuthTokenSerializer 

#####
# POST
#####

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.AllowAny,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def get_queryset(self, **kwargs):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        perm = IsOwner()

        if perm.has_permission(request=self.request, view= None ):
            return super(PostList, self).get_queryset()
        else:
            return Post.objects.filter(category_id=kwargs['category'])

from rest_framework.parsers import *
class CreateImage(generics.CreateAPIView):
    queryset = PostImage.objects.all()
    serializer_class = ImageSerializer 
    # permission_classes = (permissions.IsAuthenticated,)
    permission_classes = (permissions.AllowAny,)
    # authentication_classes = [TokenAuthentication, BasicAuthentication]
    def post(self, request, *args, **kwargs):
        
        serializer = CreateImage.serializer_class(data=request.data, context={"request": request} )
        if serializer.is_valid():
            # post = serializer.create(request.data, request.user)
            post = serializer.save()
            # serializer.create()
            # post = Post.objects.create(title = request.data['title'], category=PostCategory.objects.get(id=request.data['category']),  author = request.user, contents = request.data['contents'])
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(status = status.HTTP_400_BAD_REQUEST)


class CreatePost(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]
    def post(self, request, *args, **kwargs):
        request.data._mutable = True
        request.data['author'] = str(request.user.id)
        print("req :", request.data)
        l = []
        for img in request.data.pop('images') :
            # l.append({"image":img})
            qq = QueryDict(mutable=True)
            qq['image']=img
            l.append(qq)
            # request.data['images'].append(qq)
        print("ttest", l)
        # request.data['images']=l
        request.data.setlist('images', l)
        serializer = PostCreateSerializer(data = request.data)
        print('tt')
        if serializer.is_valid():
            # post = serializer.create(request.data, request.user)
            post = serializer.save()
            # serializer.create()
            # post = Post.objects.create(title = request.data['title'], category=PostCategory.objects.get(id=request.data['category']),  author = request.user, contents = request.data['contents'])
            return Response(serializer.data, status = status.HTTP_200_OK)

        return Response(status = status.HTTP_400_BAD_REQUEST)

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    authentication_classes = [TokenAuthentication, BasicAuthentication]


    def get(self, request, *args, **kwargs):
        """
            GET
        """
        return self.retrieve(request, *args, **kwargs)
        serializer = PostDetail.serializer_class(data = request.data)
        if serializer.is_valid():
            post = Post.objects.get()
            return Response(None, status.HTTP_200_OK)
        return Response(None, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, *args, **kwargs):
    #     """

    #     """
    #     return self.update(request, *args, **kwargs)

        
    
    def patch(self, request, *args, **kwargs):
        print(request.data)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)



class PostCategoryList(generics.ListAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    permission_classes = (IsOwnerOrConditionalReadOnly,)
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        perm = IsOwner()

        if perm.has_permission(request=self.request, view= None ):
            print("cate")
            return super(PostCategoryList, self).get_queryset()
        else:
            print("cu")
            return super(PostCategoryList, self).get_queryset()
            return PostCategory.objects.filter(is_private=False)



class PostCategoryCreate(generics.CreateAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategoryCreateSerializer
    permission_classes = (permissions.IsAuthenticated, )
    authentication_classes = [TokenAuthentication, BasicAuthentication]

    def post(self, request, *args, **kwargs):
        print('res', request.data)

        serializer = PostCategoryCreateSerializer(data= request.data)
        print(serializer.is_valid())
        if serializer.is_valid():
            # post_category = PostCategory.objects.create(name = request.data['name'],\
            #                                             is_private=request.data['is_private'],\
            #                                             parent_category = request.data.get('parent_category', 'null') )m
            serializer.create(request.data)
            return Response(serializer.data, status = status.HTTP_200_OK)
        return Response(serializer.data, status = status.HTTP_400_BAD_REQUEST)

class PostCategoryRetriveUpdateDestroy(generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = PostCategory.objects.all()
    serializer_class = PostCategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = [TokenAuthentication, ]


    def put(self, request, *args, **kwargs):
        """

        """
        return self.update(request, *args, **kwargs)
    
    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
