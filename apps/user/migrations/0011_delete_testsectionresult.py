# Generated by Django 5.1.3 on 2024-12-06 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_remove_result_quantity_result_incorrect_result_unit'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TestSectionResult',
        ),
    ]
