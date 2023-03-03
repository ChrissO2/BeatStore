from django.urls import path
from . import views


urlpatterns = [
    path('', views.index),
    path('contact/', views.ContactFormView.as_view()),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('about-me/', views.about_me_view),
    path('update-item/', views.update_item, name='update-item'),
    path('register/', views.register_view, name='register'),
    path('login/', views.LoginFormView.as_view(), name='login'),
    path('logout/', views.log_out_view, name='logout'),
    path('cart/', views.cart_view, name='cart'),
]
