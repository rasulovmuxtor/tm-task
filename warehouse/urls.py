from django.urls import path

from warehouse import views

urlpatterns = [
    path('products/', views.ProductListAPIView.as_view()),
    path('products/create/materials/', views.ProductMaterialAPIView.as_view()),
]
