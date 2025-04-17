from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from .models import Recipe

def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})