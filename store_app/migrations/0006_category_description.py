# Generated by Django 4.0.6 on 2022-07-12 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0005_rename_clothingproductimages_clothingproductimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
