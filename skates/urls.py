from django.urls import path

from skates.views import *

urlpatterns = [
    path('', index, name='index'),
]
