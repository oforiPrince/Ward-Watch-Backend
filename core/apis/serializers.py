from rest_framework import serializers

from accounts.models import Profile, Parent, Child, ParentChild, ChildLocation


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'email','role', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
        
class ParentRegisterSerializer(serializers.ModelSerializer):
    profile = UserSerializer()
    class Meta:
        model = Parent
        fields = '__all__'
        
        
        
class ChildLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildLocation
        fields = '__all__'
        
class ChildSerializer(serializers.ModelSerializer):
    profile = UserSerializer()
    location = ChildLocationSerializer()
    class Meta:
        model = Child
        fields = '__all__'
        
        
# class ParentChildSerializer(serializers.ModelSerializer):
#     parent = ParentRegisterSerializer()
#     child = ChildSerializer()
#     class Meta:
#         model = ParentChild
#         fields = '__all__'

# class LoginSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ['username', 'password']
#         extra_kwargs = {'password': {'write_only': True}}