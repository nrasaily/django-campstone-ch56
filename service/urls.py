
from django.urls import path
from . import views

urlpatterns = [
    path('', views.service_list, name='list'),
    path('<slug:slug>/', views.service_detail, name='detail'),
    path('<slug:slug>/pay/', views.service_pay, name='pay'),
    path('payment/success/', views.payment_success, name='payment_success'),
    path('payment/cancel/', views.payment_cancel, name='payment_cancel'),
    # path("<slug:slug>/process/", views.process_payment, name="process_payment"),
]
