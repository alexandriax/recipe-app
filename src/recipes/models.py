from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=100)
    cooking_time = models.PositiveIntegerField()
    ingredients = models.ManyToManyField('ingredients.Ingredient')  
    difficulty = models.CharField(max_length=20, blank=True, editable=False)

    def calculate_difficulty(self):
        if self.cooking_time < 10 and self.ingredients.count() < 4:
            return 'Easy'
        elif self.cooking_time < 10 and self.ingredients.count() >= 4:
            return 'Medium'
        elif self.cooking_time >= 10 and self.ingredients.count() < 4:
            return 'Intermediate'
        else:
            return 'Hard'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  
        self.difficulty = self.calculate_difficulty()
        super().save(update_fields=['difficulty'])

    def __str__(self):
        return self.name



