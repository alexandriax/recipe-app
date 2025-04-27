from django import forms
from .models import Recipe

CHART_CHOICES = (
    ('#1', 'Bar Chart'),
    ('#2', 'Pie Chart'),
    ('#3', 'Line Chart'),
)

class RecipeSearchForm(forms.Form):
    query = forms.CharField(
        label='Search Recipes',
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'Search recipes...'})
    )
    chart_type = forms.ChoiceField(
        choices=CHART_CHOICES,
        widget=forms.Select(),
        label='Chart Type'
    )

class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(
        help_text="Separate ingredients with commas (e.g., sugar, flour, water)"
    )

    class Meta:
        model = Recipe
        fields = ['name', 'cooking_time', 'ingredients', 'instructions', 'image']
