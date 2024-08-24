# Generated by Django 5.0.6 on 2024-08-24 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_cartitem_promotion'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('card', 'Card'), ('cash', 'Cash')], default=1, max_length=10),
            preserve_default=False,
        ),
    ]
