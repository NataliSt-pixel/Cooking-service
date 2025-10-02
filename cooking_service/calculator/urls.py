from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),  # главная страница
    path('<str:dish>/', views.recipe_view, name='recipe'),  # страница рецепта
]