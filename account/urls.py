from django.urls import path, include
from . import views
app_name = "account"
urlpatterns = [
    path('login/', views.login, name="login"),
    path('login/registration/', views.registration, name="registration"),
    path('order/', views.show_order, name="show_order"),
]
#registration