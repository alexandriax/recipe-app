from django.test import TestCase
from src.recipes.models import Recipe
from .models import Ingredient

class IngredientModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Vegan Pancakes",
            cooking_time=20,
            difficulty="Medium"
        )
        self.ingredient = Ingredient.objects.create(
            name="Almond Milk",
            recipe=self.recipe
        )

    def test_ingredient_creation(self):
        self.assertEqual(self.ingredient.name, "Almond Milk")
        self.assertEqual(self.ingredient.recipe, self.recipe)
        self.assertEqual(str(self.ingredient), "Almond Milk")

    def test_recipe_ingredient_relationship(self):
        ingredients = self.recipe.ingredients.all()
        self.assertIn(self.ingredient, ingredients)
