from django.urls import path
from . import views

app_name = 'adminsite'
urlpatterns = [
    path('add_product/', views.add_product, name="add_product"),
    path('get_category/', views.get_category, name="get_category"),
    path('get_category/show_product/', views.show_product, name="show_product"),
    path('get_category/show_product/update_product/<int:id>/', views.update_product, name="update_product"),
]
