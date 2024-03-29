# Generated by Django 3.2.12 on 2024-02-26 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Authentication', '0003_user_is_verified_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bank_details',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='id_proof',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='ifsc_code',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_creator',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='payment_made',
            field=models.BooleanField(default=False),
        ),
    ]
