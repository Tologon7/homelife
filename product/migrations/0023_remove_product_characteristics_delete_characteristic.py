# Generated by Django 5.1.2 on 2024-10-29 08:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0022_alter_product_characteristics'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='characteristics',
        ),
        migrations.DeleteModel(
            name='Characteristic',
        ),
    ]