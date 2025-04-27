from django.urls import path
from . import views

app_name = 'recipes'

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('list/<int:pk>/', views.recipe_detail, name='detail'),
    path('search/', views.recipe_search, name='recipe_search'),
    path('about/', views.about, name='about'),
    path('add/', views.add_recipe, name='add_recipe'),

]
