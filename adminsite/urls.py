from django.urls import path
from .views import order_details, admin_options, add_coupon, add_product, get_category, show_product, update_product, get_coupon, show_all_order
app_name = 'adminsite'
urlpatterns = [
    path('adminOptions/', admin_options,name="adminOptions"),
    path('adminOptions/addCoupon/', add_coupon, name='addCoupon'),
    path('adminOptions/getCoupon/', get_coupon, name='getCoupon'),
    path('adminOptions/allOrder/',show_all_order,name='allOrder'),
    path('adminOptions/allOrder/orderDetails/<int:id>/', order_details, name='orderDetails'),
    path('adminOptions/add_product/', add_product, name="add_product"),
    path('adminOptions/get_category/', get_category, name="get_category"),
    path('adminOptions/get_category/show_product/', show_product, name="show_product"),
    path('adminOptions/get_category/show_product/update_product/<int:id>/', update_product, name="update_product"),
]
