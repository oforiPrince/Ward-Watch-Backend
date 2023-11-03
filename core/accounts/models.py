from django.db import models
from django.contrib.auth.models import AbstractBaseUser 
from accounts.managers import UserManager

from core.utils.enums import Gender  

class Profile(AbstractBaseUser):
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    role = models.CharField(max_length=10, choices=[('parent', 'Parent'), ('child', 'Child')], default='child')
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    # Configure the custom user manager
    objects = UserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    def get_short_name(self):
        return self.first_name
    

class Parent(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.profile)


class Child(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    location = models.OneToOneField('ChildLocation', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return self.profile.full_name
    
class ChildLocation(models.Model):
    longitude = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitudeDelta = models.CharField(max_length=100)
    latitudeDelta = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.longitude} - {self.latitude}"
    
class ParentChild(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.parent} - {self.child}"