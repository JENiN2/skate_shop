from django.urls import path

from skates.views import *

urlpatterns = [
    path('', index, name='index'),
    path('list', skates_list, name='skates_list'),
    path('list/<int:skate_id>/', skate_detail, name='skate_detail'),
    path('add_new', skate_add, name='skate_add'),
]
