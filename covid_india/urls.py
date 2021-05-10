
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('state', views.state, name='state'),
    path('/<str:statename>/district', views.district, name='district'),
]
