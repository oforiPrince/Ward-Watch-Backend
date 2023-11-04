from django.db import models
from django.contrib.auth.models import AbstractBaseUser 
from accounts.managers import UserManager

import uuid
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
        return self.username
    

class Parent(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.profile)


class Child(models.Model):
    def unique_id_generator(self):
        return uuid.uuid4().hex[:6].upper()
    
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    unique_id = models.CharField(max_length=6, unique=True, blank=True, null=True)
    location = models.OneToOneField('ChildLocation', on_delete=models.CASCADE, blank=True, null=True)
    
    def __str__(self):
        return str(self.profile)
    
    def save(self, *args, **kwargs):
        if self.location and not self.unique_id:
            self.unique_id = self.unique_id_generator()
        super().save(*args, **kwargs)
        
class ChildLocation(models.Model):
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitudeDelta = models.DecimalField(max_digits=9, decimal_places=6)
    latitudeDelta = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return f"{self.longitude} - {self.latitude}"
    
class ParentChild(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.parent} - {self.child}"