from django.urls import path

from orders import views

urlpatterns = [
    path('orders/', views.order, name='order_api'),
]
