from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import Recipe
from ingredients.models import Ingredient  

class RecipeModelTest(TestCase):

    def setUp(self):
        self.recipe = Recipe.objects.create(
            name="Vegan Mac & Cheese",
            cooking_time=30,
            instructions="Boil pasta, blend cashews, mix together.",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

        # Add ingredients to test difficulty calculation
        i1 = Ingredient.objects.create(name="Cashews")
        i2 = Ingredient.objects.create(name="Pasta")
        i3 = Ingredient.objects.create(name="Nutritional Yeast")
        i4 = Ingredient.objects.create(name="Garlic Powder")
        self.recipe.ingredients.set([i1, i2, i3, i4])
        self.recipe.save()

        self.recipe_no_image = Recipe.objects.create(
            name="Mystery Dish",
            cooking_time=5,
            instructions="???"
        )

    def test_recipe_creation(self):
        self.assertEqual(self.recipe.name, "Vegan Mac & Cheese")
        self.assertEqual(self.recipe.cooking_time, 30)
        self.assertEqual(str(self.recipe), "Vegan Mac & Cheese")

    def test_difficulty_calculation(self):
        self.assertEqual(self.recipe.difficulty, "Hard")  # >10 min + ≥4 ingredients

    def test_get_absolute_url(self):
        self.assertEqual(self.recipe.get_absolute_url(), f"/list/{self.recipe.pk}/")

class RecipeViewsTest(TestCase):

    def setUp(self):
        # Recipe with image
        self.recipe_with_image = Recipe.objects.create(
            name="Chickpea Salad",
            cooking_time=10,
            instructions="Mix chickpeas with veggies and dressing.",
            image=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')
        )

        # Recipe without image
        self.recipe_no_image = Recipe.objects.create(
            name="Mystery Stew",
            cooking_time=5,
            instructions="Just vibes."
        )

    def test_recipe_list_view(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chickpea Salad")
        self.assertContains(response, "Mystery Stew")

    def test_recipe_detail_view(self):
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe_with_image.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Chickpea Salad")

    def test_recipe_with_image(self):
        self.assertIsNotNone(self.recipe_with_image.image)
        self.assertTrue(self.recipe_with_image.image.name.startswith('recipes/'))


    def test_recipe_no_image_uses_default(self):
        self.assertEqual(self.recipe_no_image.image.name, 'no_picture.png')

    def test_no_image_fallback_in_template(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'no_picture.png')  # fallback image


