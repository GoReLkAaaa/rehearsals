from django.urls import path
from . import views


urlpatterns = [
    path('products/', views.ProductViewSet.as_view(
        {
            'get': 'list',
        }
    )),
    path('products/<int:pk>/', views.ProductViewSet.as_view(
        {
            'get': 'retrieve',
        }
    )),
    path('users-profile/', views.UserProfileViewSet.as_view(
        {
            'get': 'list',
        }
    )),
    path('users-profile/<int:pk>/', views.UserProfileViewSet.as_view(
        {
            'get': 'retrieve',
        }
    )),
    path('cart-items/', views.CartItemViewSet.as_view(
        {
            'get': 'list',
            'post': 'create',
        }
    )),
    path('cart-items/<int:pk>/', views.CartItemViewSet.as_view(
        {
            'get': 'retrieve',
            'delete': 'destroy',
        }
    ))
]
