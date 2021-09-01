from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path('', views.home, name="home"),
    path('login/', views.loginPage, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('products/', views.products, name="products"),
    path('customer/<str:pk_test>/', views.customer, name="customer"),
    path('create_order/', views.createOrder, name="create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name="update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name="delete_order")

]