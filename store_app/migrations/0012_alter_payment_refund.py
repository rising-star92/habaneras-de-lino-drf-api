# Generated by Django 4.0.6 on 2022-08-28 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0011_address_payment_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='refund',
            field=models.CharField(choices=[('NO REFUND ASKED', 'NO REFUND ASKED'), ('REFUND REQUESTED', 'REFUND REQUESTED'), ('REFUND MADE', 'REFUND MADE'), ('REFUND FAILED', 'REFUND FAILED')], default='NO REFUND ASKED', max_length=256),
        ),
    ]
