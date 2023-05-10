from django.urls import path

from skates.views import *

urlpatterns = [
    path('', index, name='index'),
    path('list', skates_list, name='skates_list'),
]
