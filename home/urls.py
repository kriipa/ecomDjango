from django.urls import path, include
from .views import *

urlpatterns = [
    path("", Homeview.as_view(), name='home'),
]
