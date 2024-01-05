from django.urls import path
from . import views

urlpatterns = [
    path('',views.Login,name='login'),
    path('logout',views.Logout,name='Logout'),
    path('register',views.AccountRegistration.as_view(),name='register'),
    path('home',views.home,name='home'),
]