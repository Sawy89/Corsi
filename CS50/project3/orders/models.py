from django.db import models
from django.contrib.auth.models import User
from enum import Enum

# Create your models here.
class DishCategory(models.Model):
    '''
    Class for dish category (pizza, pasta, ..)
    '''
    name = models.CharField(max_length=64)
    description = models.CharField(max_length=1024)

    def __str__(self):
        return f"{self.name}"


class Dish(models.Model):
    '''
    Class for all dish, related to the dish category
    '''
    name = models.CharField(max_length=64)
    category = models.ForeignKey(DishCategory, on_delete=models.CASCADE, related_name="dish")
    number_available_toppings = models.IntegerField()

    def __str__(self):
        return f"{self.category}: {self.name}"
    
    # def getDimension():


class DishPrice(models.Model):
    '''
    Class for different dimension of a dish
    '''

    class DimensionType(models.TextChoices):
        '''
        Dimensions available
        https://stackoverflow.com/questions/54802616/how-to-use-enums-as-a-choice-field-in-django-model
        https://docs.djangoproject.com/en/dev/ref/models/fields/#field-choices-enum-types
        '''
        SMALL = "S"
        NORMAL = "M"
        LARGE = "L"

    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="dimension")
    dimension = models.CharField(max_length=1, choices=DimensionType.choices, 
                            default=DimensionType.NORMAL)
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return f"{self.dish} - {self.dimension}: {self.price}€"


class Topping(models.Model):
    '''
    Class for listing the different toppings
    '''
    name = models.CharField(max_length=64)
    def __str__(self):
        return f"{self.name}"


class Addition(models.Model):
    '''
    Class for addition to some dish
    '''
    name = models.CharField(max_length=64)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    dish = models.ManyToManyField(Dish, blank=True, related_name='addition')

    def __str__(self):
        return f"+{self.name} [{self.dish}] = +{self.price}€"


class Orders(models.Model):
    '''
    Class for saving users order
    '''
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)
    insertdate = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False)
    insertdate_completed = models.DateTimeField(default=None, null=True)


class OrdersDish(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE) 
    dish_price = models.ForeignKey(DishPrice, on_delete=models.DO_NOTHING)
    total_price = models.DecimalField(max_digits=6, decimal_places=2)


class OrdersTopping(models.Model):
    order_dish = models.ForeignKey(OrdersDish, on_delete=models.CASCADE)
    topping = models.ForeignKey(Topping, on_delete=models.DO_NOTHING)


class OrdersAddition(models.Model):
    order_dish = models.ForeignKey(OrdersDish, on_delete=models.CASCADE)
    addition = models.ForeignKey(Addition, on_delete=models.DO_NOTHING)
