from django.test import TestCase
from .models import Recipe

class RecipeModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Vegan Mac & Cheese",
            cooking_time=30,
            difficulty="Easy"
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Vegan Mac & Cheese")
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(self.recipe.difficulty, "Easy")
        self.assertEqual(str(self.recipe), "Vegan Mac & Cheese")
