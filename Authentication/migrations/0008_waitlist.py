# Generated by Django 5.0.3 on 2024-03-25 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0007_alter_virtuallytried_cloth_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Waitlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
