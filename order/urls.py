from django.urls import path, include
from . import views

urlpatterns = [
    path('cart/<int:id>', views.addtocart, name="addtocart"),
    path('showcart/', views.showcart, name="showcart"),
    path('update_add_single_element/<int:id>', views.update_add_single_element, name="update_add_single_element"),
    path('update_delete_single_element/<int:id>', views.update_delete_single_element,
         name="update_delete_single_element"),
    path('delete_from_cart/<int:id>', views.delete_from_cart, name="delete_from_cart")
]
