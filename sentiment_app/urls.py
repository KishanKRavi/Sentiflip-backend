from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.search_products, name='search_products'),
    path('analyze/', views.analyze_product_reviews, name='analyze_product_reviews'),
    path('gemini/', views.geminiAPI, name='geminiAPI'),
]
