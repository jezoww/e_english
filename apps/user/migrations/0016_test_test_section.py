# Generated by Django 5.1.3 on 2024-12-09 09:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0015_testsection_remove_test_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='test',
            name='test_section',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='user.testsection'),
            preserve_default=False,
        ),
    ]