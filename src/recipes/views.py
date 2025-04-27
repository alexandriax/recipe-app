from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from .models import Recipe
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RecipeSearchForm
import pandas as pd
from .utils import get_chart
from django.db.models import Q
from django.contrib import messages
from .forms import RecipeForm
from ingredients.models import Ingredient






def home(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipes_home.html', {'recipes': recipes})

@login_required
def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, 'recipes/recipe_list.html', {'recipes': recipes})

@login_required
def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    return render(request, 'recipes/recipe_detail.html', {'recipe': recipe})

@login_required
def recipe_search(request):
    form = RecipeSearchForm(request.GET or None)
    results = None
    results_table = None
    chart = None 

    if request.method == 'GET' and form.is_valid():
        query = form.cleaned_data['query']
        chart_type = form.cleaned_data['chart_type']
        results = Recipe.objects.filter(
          Q(name__icontains=query) | Q(ingredients__name__icontains=query)
        ).distinct()

        if results:
            df = pd.DataFrame(results.values('name', 'cooking_time', 'difficulty'))
            results_table = df.to_html(index=False)
            chart = get_chart(chart_type, df)

    return render(request, 'recipes/search.html', {
        'form': form,
        'results': results,
        'results_table': results_table,
        'chart': chart  

    })

def about(request):
    return render(request, 'recipes/about.html')


@login_required
def add_recipe(request):
    if request.method == 'POST':
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)  # don't save yet
            recipe.save()

            # Process the ingredients
            ingredients_text = form.cleaned_data['ingredients']
            ingredient_names = [name.strip().lower() for name in ingredients_text.split(',')]

            for name in ingredient_names:
                ingredient_obj, created = Ingredient.objects.get_or_create(name=name)
                recipe.ingredients.add(ingredient_obj)

            return redirect('recipes:recipe_list')  # or wherever you want
    else:
        form = RecipeForm()

    return render(request, 'recipes/add_recipe.html', {'form': form})



def login_view(request):
    error_message = None
    form = AuthenticationForm()

    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('recipes:recipe_list')
            else:
                error_message = 'Invalid credentials, try again.'
        else:
            error_message = 'Form error, please check your input.'

    return render(request, 'auth/login.html', {'form': form, 'error_message': error_message})

def logout_view(request):
    logout(request)
    return render(request, 'auth/logout.html')
