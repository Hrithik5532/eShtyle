# Generated by Django 4.2.4 on 2024-02-25 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='sqp',
        ),
        migrations.AddField(
            model_name='cart',
            name='sqp',
            field=models.ManyToManyField(to='Products.sqp'),
        ),
    ]
