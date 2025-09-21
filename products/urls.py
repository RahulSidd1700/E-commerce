from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('product/<int:pk>/', views.product_detail, name='product_detail'),
    path('add-to-cart/<int:pk>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('update-cart/<int:pk>/', views.update_cart_item, name='update_cart_item'),
    path('remove/<int:pk>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('api/products/', views.api_product_list),
    path('api/add-product/', views.ProductCreateView.as_view()),
    path('order-history/', views.order_history, name='order_history'),
    path('admin/products/', views.admin_products, name='admin_products'),
    path('admin/products/add/', views.add_product, name='add_product'),
    path('admin/products/edit/<int:pk>/', views.edit_product, name='edit_product'),
    path('admin/products/delete/<int:pk>/', views.delete_product, name='delete_product'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)