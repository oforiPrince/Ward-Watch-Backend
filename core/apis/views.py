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
        
class ChildLocationAPI(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChildLocationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        # Get the child
        child = Child.objects.get(profile=request.user)
        # Check if child exists
        if child is not None:
            # Check if child has a location
            if child.location is not None:
                # Update the location
                child.location.longitude = serializer.validated_data['longitude']
                child.location.latitude = serializer.validated_data['latitude']
                child.location.longitudeDelta = serializer.validated_data['longitudeDelta']
                child.location.latitudeDelta = serializer.validated_data['latitudeDelta']
                child.location.save()
                response_data = {
                    "message": "Location updated successfully.",
                    "data": ChildSerializer(child).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                # Create the location
                location = ChildLocation.objects.create(
                    longitude=serializer.validated_data['longitude'],
                    latitude=serializer.validated_data['latitude'],
                    longitudeDelta=serializer.validated_data['longitudeDelta'],
                    latitudeDelta=serializer.validated_data['latitudeDelta']
                )
                child.location = location
                child.save()
                response_data = {
                    "message": "Location created successfully.",
                    "data": ChildSerializer(child).data,
                }
                return Response(response_data, status=status.HTTP_200_OK)
            
        else:
            response_data = {
                "message": "Child not found.",
                "data": None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        

class ParentLinkChild(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParentChildSerializer
    
    def post(self, request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        
        try:
            # Get the child
            child = Child.objects.get(unique_id=unique_id)
            
            # Check if child exists
            if child is not None:
                # Check if child has a parent
                if child.parentchild_set.all().exists():
                    response_data = {
                        "message": "Child already has a parent.",
                        "data": None,
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
                else:
                    # Create the parent-child relation
                    parent = Parent.objects.get(profile=request.user)
                    parent_child = ParentChild.objects.create(parent=parent, child=child)
                    
                    # Serialize child's profile and location data
                    child_serializer = ChildSerializer(child)
                    
                    response_data = {
                        "message": "Child linked to parent successfully.",
                        "data": child_serializer.data
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
            
            else:
                response_data = {
                    "message": "Child not found.",
                    "data": None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except Child.DoesNotExist:
            response_data = {
                "message": "Child not found.",
                "data": None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
class ParentUnlinkChild(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ParentChildSerializer
    
    def post(self, request, *args, **kwargs):
        unique_id = request.data.get('unique_id')
        
        try:
            # Get the child
            child = Child.objects.get(unique_id=unique_id)
            
            # Check if child exists
            if child is not None:
                # Check if child has a parent
                if child.parentchild_set.all().exists():
                    # Delete the parent-child relation
                    parent_child = ParentChild.objects.get(child=child)
                    parent_child.delete()
                    
                    # Serialize child's profile and location data
                    child_serializer = ChildSerializer(child)
                    
                    response_data = {
                        "message": "Child unlinked from parent successfully.",
                        "data": child_serializer.data
                    }
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    response_data = {
                        "message": "Child does not have a parent.",
                        "data": None,
                    }
                    return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            
            else:
                response_data = {
                    "message": "Child not found.",
                    "data": None,
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        
        except Child.DoesNotExist:
            response_data = {
                "message": "Child not found.",
                "data": None,
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
        