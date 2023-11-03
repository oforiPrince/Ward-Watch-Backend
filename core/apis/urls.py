from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/',views.RegisterAPI.as_view()),
    path('auth/login/',views.LoginAPI.as_view()),
    # path('auth/login/child',views.ChildLoginAPI.as_view()),
]