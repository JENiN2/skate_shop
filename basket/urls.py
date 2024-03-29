from django.urls import path

from .views import basket_add, basket_info, basket_clear, basket_remove

urlpatterns = [
    path('', basket_info, name='list_basket_prod'),
    path('add/<int:product_id>', basket_add, name='add_basket_prod'),
    path('remove/<int:product_id>', basket_remove, name='remove_basket_prod'),
    path('clear/', basket_clear, name='clear_basket_prod'),
]
