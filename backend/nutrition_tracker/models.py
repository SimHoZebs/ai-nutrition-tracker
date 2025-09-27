from django.db import models

class CustomFood(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    serving_size = models.DecimalField(max_digits=10, decimal_places=2, help_text="Serving size in grams")
    calories = models.DecimalField(max_digits=10, decimal_places=2)
    protein = models.DecimalField(max_digits=10, decimal_places=2)
    carbohydrates = models.DecimalField(max_digits=10, decimal_places=2)
    fat = models.DecimalField(max_digits=10, decimal_places=2)
    trans_fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    saturated_fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unsaturated_fat = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    micros = models.JSONField(default=dict, blank=True, help_text="Micro nutrients as JSON, e.g., {'vitamin_a': 10.5}")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

