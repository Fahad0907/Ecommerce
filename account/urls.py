from django.urls import path, include
from account.views import logout, login, registration, userProfile, order_details_for_user, details_order_show
app_name = "account"
urlpatterns = [
    path('logout/', logout, name="logout"),
    path('login/', login, name="login"),
    path('userProfile/', userProfile, name='userProfile'),
    path('userProfile/userOrderDetails/',order_details_for_user,name = 'userOrderDetails'),
    path('userProfile/userOrderDetails/show/<int:id>/',details_order_show,name = 'show'),
    path('login/registration/', registration, name="registration"),

    
    
]
#registration