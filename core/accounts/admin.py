from django.contrib import admin

from accounts.models import Profile, Parent, Child, ParentChild, ChildLocation

admin.site.site_header = "Ward Watch Admin"
admin.site.site_title = "Ward Watch Admin Portal"
admin.site.index_title = "Welcome to Ward Watch Portal"

# Register your models here.
admin.site.register(Profile)
admin.site.register(Parent)
admin.site.register(Child)
admin.site.register(ParentChild)
admin.site.register(ChildLocation)