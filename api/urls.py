from django.urls import path, include
from .views import UserRegistrationView, LoginView, ProductCreateView,ProductListView, ProductUpdateView, ProductDetailView, ProductDeleteView
urlpatterns = [
      path('api/register', UserRegistrationView.as_view()),
      path('api/login', LoginView.as_view()),
      path('api/products', ProductListView.as_view()),
      path('api/product/create', ProductCreateView.as_view()),
      path('api/products/<int:pk>/update', ProductUpdateView.as_view(), name='product-update'),
      path('api/products/<int:pk>/detail', ProductDetailView.as_view(), name='product-detail'),
      path('api/products/<int:pk>/delete', ProductDeleteView.as_view(), name='product-delete'),
]