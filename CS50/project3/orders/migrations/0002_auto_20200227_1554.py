# Generated by Django 3.0.3 on 2020-02-27 15:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DishPrices',
            new_name='DishPrice',
        ),
        migrations.RenameModel(
            old_name='Toppings',
            new_name='Topping',
        ),
        migrations.RenameField(
            model_name='dish',
            old_name='n_toppings',
            new_name='number_available_toppings',
        ),
    ]
