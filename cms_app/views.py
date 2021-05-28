from django.shortcuts import render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import Group
from django.views.generic.base import View
from rest_framework import status
from rest_framework import viewsets
from rest_framework import filters
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import UserRegister, ContentItem
from .serializers import UserRegisterSerializer, LoginSerializer, ContentSerializer
from .permissions import UpdateOwnContent, AdminOnly


class RegisterUserView(APIView):
    permission_classes = ([AllowAny])

    def post(self, request):
        
        serializer = UserRegisterSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = "successfully register a new user."
            data['email'] = user.email
            token = Token.objects.get(user=user).key
            data['token'] = token
            my_group, created = Group.objects.get_or_create(name='Author')
            my_group.user_set.add(user)
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = ([AllowAny])

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)

        user = authenticate(request, username = request.data['email'], password = request.data['password'])

        if user:
            login(request, user)
            token = Token.objects.filter(user=user).first()
            if token:
                token.delete()
            token = Token.objects.create(user=user)
            user_token = token.key
            data = {
                'email': request.data['email'],
                'auth_token': user_token
            }
            return Response(data, status=status.HTTP_200_OK)
        return Response({'message': 'Username or Password Incorrect!'}, status=status.HTTP_404_NOT_FOUND)


class LogoutView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = [(IsAuthenticated)]
    serailizer_class = LoginSerializer

    def post(self, request):
        token = request.auth
        # print(token)
        try: 
            token = Token.objects.get(key=token).delete()
            logout(request)
        except:
            return Response({"error": "session1 does not exists."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


class AddContent(viewsets.ModelViewSet):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    # queryset = ContentItem.objects.all()
    serializer_class = ContentSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('title', 'body', 'summary', 'category')

    def get_queryset(self):
        if self.request.user.is_superuser == True:
            return ContentItem.objects.all()
        else:
            return ContentItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)