# Generated by Django 5.0.3 on 2024-03-22 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0006_user_full_body_image_virtuallytried'),
    ]

    operations = [
        migrations.AlterField(
            model_name='virtuallytried',
            name='cloth_image',
            field=models.ImageField(blank=True, null=True, upload_to='cloth_image/'),
        ),
    ]
