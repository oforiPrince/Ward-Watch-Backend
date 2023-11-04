from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/',views.RegisterAPI.as_view()),
    path('auth/login/',views.LoginAPI.as_view()),
    path('child/location/',views.ChildLocationAPI.as_view()),
    path('parent/child/link',views.ParentLinkChild.as_view()),
    path('parent/child/unlink',views.ParentUnlinkChild.as_view()),
]