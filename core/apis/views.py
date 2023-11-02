from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import authenticate

from apis.serializers import *

class ParentRegisterAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ParentRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create the parent account
            parent = serializer.save()
            parent.profile.is_parent = True
            parent.profile.save()
            user = parent.profile
            
            response_data = {
                "message": "Parent account created successfully.",
                "data": ParentRegisterSerializer(parent, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_messages = []
            for field, error_list in errors.items():
                for error in error_list:
                    error_messages.append(error)
            response_data = {
                "message": error_messages,
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ParentLoginAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        print('username: ', username, 'password: ', password )
        print(username, password)
        user = authenticate(username=username, password=password)
        if user:
            parent = ParentRegisterSerializer(user.parent)
            response_data = {
                "message": "Parent logged in successfully.",
                "data": parent.data,
                "token": AuthToken.objects.create(user)[1]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "message": "Invalid username or password.",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ChildRegisterAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = ChildSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            # Create the child account
            child = serializer.save()
            child.profile.is_child = True
            child.profile.save()
            user = child.profile
            
            response_data = {
                "message": "Child account created successfully.",
                "data": ChildSerializer(child, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1]
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        else:
            errors = serializer.errors
            error_messages = []
            for field, error_list in errors.items():
                for error in error_list:
                    error_messages.append(error)
            response_data = {
                "message": error_messages,
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ChildLoginAPI(generics.GenericAPIView):
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            child = ChildSerializer(user.child)
            response_data = {
                "message": "Child logged in successfully.",
                "data": child.data,
                "token": AuthToken.objects.create(user)[1]
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "message": "Invalid username or password.",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)