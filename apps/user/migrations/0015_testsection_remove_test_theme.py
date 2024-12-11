# Generated by Django 5.1.3 on 2024-12-09 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0014_test_theme'),
    ]

    operations = [
        migrations.CreateModel(
            name='TestSection',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='test',
            name='theme',
        ),
    ]