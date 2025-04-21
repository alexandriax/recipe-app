from django import forms

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
