# Generated by Django 5.1.2 on 2024-11-25 08:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_gender_label_alter_gender_value'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gender',
            name='label',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='gender',
            name='value',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
