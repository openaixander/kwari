from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout_view, name='checkout'),
    path('verify-payment/', views.verify_payment_view, name='verify_payment'),
    path('success/', views.checkout_success_view, name='checkout_success'),
    path('order/<int:order_id>/', views.order_detail_view, name='order_detail'),
]