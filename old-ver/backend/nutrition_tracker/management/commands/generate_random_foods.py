import random
from django.core.management.base import BaseCommand
from foods.models import Food
from users.models import User


FOOD_NAMES = [
    'Apple', 'Banana', 'Chicken Breast', 'Rice', 'Salad', 'Salmon', 'Egg', 'Bread',
    'Yogurt', 'Pasta', 'Potato', 'Tomato', 'Orange', 'Milk', 'Cheese', 'Beef', 'Fish',
    'Carrot', 'Broccoli', 'Spinach', 'Oatmeal', 'Cereal', 'Peanut Butter', 'Honey'
]


class Command(BaseCommand):
    help = 'Generates and adds random foods to the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=10,
            help='Number of random foods to generate'
        )

    def handle(self, *args, **options):
        count = options['count']
        user = User.objects.get(id=1)
        
        for _ in range(count):
            name = random.choice(FOOD_NAMES)
            
            food = Food(
                name=name,
                serving_size=round(random.uniform(50, 500), 2),
                calories=round(random.uniform(1, 500), 2),
                protein=round(random.uniform(0, 50), 2),
                carbohydrates=round(random.uniform(0, 100), 2),
                trans_fat=round(random.uniform(0, 10), 2),
                saturated_fat=round(random.uniform(0, 10), 2),
                unsaturated_fat=round(random.uniform(0, 10), 2),
                meal_type=random.choice(['breakfast', 'lunch', 'dinner', 'snack', None]),
                user=user
            )
            food.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully generated and added {count} random foods to the database for user {user.username}')
        )
