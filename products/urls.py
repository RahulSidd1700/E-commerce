from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/products/', views.api_product_list),
    path('api/add-product/', views.ProductCreateView.as_view()),
]
urlpatterns += [
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/products/add/', views.add_product, name='add_product'),
    path('admin/products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('admin/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
]
