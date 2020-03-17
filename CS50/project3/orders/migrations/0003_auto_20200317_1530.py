# Generated by Django 3.0.3 on 2020-03-17 15:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('orders', '0002_auto_20200227_1554'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('insertdate', models.DateTimeField(auto_now_add=True)),
                ('completed', models.BooleanField(default=False)),
                ('insertdate_completed', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrdersDish',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_price', models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.AlterField(
            model_name='dishprice',
            name='dimension',
            field=models.CharField(choices=[('S', 'Small'), ('M', 'Normal'), ('L', 'Large')], default='M', max_length=1),
        ),
        migrations.CreateModel(
            name='OrdersTopping',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrdersDish')),
                ('topping', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.Topping')),
            ],
        ),
        migrations.AddField(
            model_name='ordersdish',
            name='dish_price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.DishPrice'),
        ),
        migrations.AddField(
            model_name='ordersdish',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.Orders'),
        ),
        migrations.CreateModel(
            name='OrdersAddition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addition', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='orders.Addition')),
                ('order_dish', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.OrdersDish')),
            ],
        ),
    ]
