# Generated by Django 4.0.6 on 2022-08-28 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0012_alter_payment_refund'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='address',
            name='zip_code',
            field=models.CharField(default='00000', max_length=5),
        ),
        migrations.AddField(
            model_name='order',
            name='commnets',
            field=models.TextField(blank=True),
        ),
    ]
