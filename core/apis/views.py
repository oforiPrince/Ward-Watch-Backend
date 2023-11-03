from rest_framework import generics, permissions, status
from rest_framework.response import Response
from knox.models import AuthToken
from django.contrib.auth import authenticate

from apis.serializers import *

class RegisterAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data['username']
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        role = serializer.validated_data['role']
        
        # Check if the username already exists
        if Profile.objects.filter(username=username).exists():
            response_data = {
                "message": "Username already exists.",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        else:
            # Create the profile
            profile = Profile(username=username, email=email, role=role)
            profile.set_password(password)
            profile.save()
            
            # Create the parent account
            if role == 'parent':
                parent = Parent.objects.create(profile=profile)
                response_data = {
                    "message": "Parent account created successfully.",
                    "data": ParentRegisterSerializer(parent).data,
                    "token": AuthToken.objects.create(profile)[1]
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            # Create the child account
            elif role == 'child':
                child = Child.objects.create(profile=profile)
                response_data = {
                    "message": "Child account created successfully.",
                    "data": ChildSerializer(child).data,
                    "token": AuthToken.objects.create(profile)[1]
                }
                return Response(response_data, status=status.HTTP_201_CREATED)
            
            else:
                response_data = {
                    "message": "Invalid role.",
                    "data": None,
                    "token": None
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class LoginAPI(generics.GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        
        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            # Create the token
            token = AuthToken.objects.create(user)[1]
            response_data = {
                "message": "Login successful.",
                "data": UserSerializer(user).data,
                "token": token
            }
            return Response(response_data, status=status.HTTP_200_OK)
        else:
            response_data = {
                "message": "Invalid credentials.",
                "data": None,
                "token": None
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)