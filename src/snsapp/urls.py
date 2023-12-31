from django.urls import path
# from .views import Home
from . import views

urlpatterns = [
    # path('', Home.as_view(), name='home'),
    path('', views.index, name='index'),
]
