# Generated by Django 5.1.3 on 2024-12-04 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='unit',
            name='name',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]