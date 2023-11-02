from rest_framework import serializers

from accounts.models import Profile, Parent, Child, ParentChild, ChildLocation

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username','first_name','other_name','last_name','gender','is_parent','is_child','password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = Profile.objects.create_user(**validated_data)
        # encrypt the password
        user.set_password(validated_data['password'])
        user.save()
        return user
        
class ParentRegisterSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = Parent
        fields = '__all__'
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile')
        profile_data['is_parent'] = True  # Set is_parent to True
        profile_serializer = ProfileSerializer(data=profile_data)
        if profile_serializer.is_valid():
            profile = profile_serializer.save()
            validated_data['profile'] = profile
            parent = super().create(validated_data)
            return parent
        else:
            raise serializers.ValidationError("Invalid profile data")
        
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
class ChildLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildLocation
        fields = '__all__'
        
class ChildSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    location = ChildLocationSerializer()
    class Meta:
        model = Child
        fields = '__all__'
        
class ParentChildSerializer(serializers.ModelSerializer):
    parent = ParentRegisterSerializer()
    child = ChildSerializer()
    class Meta:
        model = ParentChild
        fields = '__all__'

