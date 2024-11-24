# Generated by Django 5.1.2 on 2024-11-23 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_remove_gender_title_gender_name_user_role'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gender',
            old_name='name',
            new_name='label',
        ),
        migrations.AddField(
            model_name='gender',
            name='value',
            field=models.CharField(default=1, max_length=10),
            preserve_default=False,
        ),
    ]