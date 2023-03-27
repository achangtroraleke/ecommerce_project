from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('create-sale/', views.createSale, name='create-sale'),
    path('item-page/<str:pk>', views.itemPage, name ='item-page'),
    path('cart', views.cartPage, name='cart'),
    path('add-item/<str:pk>', views.addItem, name='add-item'),
    path('checkout/', views.checkout, name='check-out'),

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register')
]