from django.db import models


class Food(models.Model):
    name = models.CharField(max_length=255)
    serving_size = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Serving size in grams"
    )
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    protein = models.DecimalField(max_digits=10, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=10, decimal_places=2)
    trans_fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saturated_fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unsaturated_fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    others = models.JSONField(
        default=dict,
        blank=True,
        help_text="Micro nutrients as JSON, e.g., {'vitamin_a': 10.5}",
    )
    meal_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
