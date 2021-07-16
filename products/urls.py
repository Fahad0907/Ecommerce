from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homePage, name="homepage"),
    path('showproduct/<int:id>/', views.showProduct, name="showProduct"),
    path('productdetails/<int:id>/', views.productDetails, name='productDetails'),

]