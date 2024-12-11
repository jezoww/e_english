# Generated by Django 5.1.3 on 2024-12-06 10:40

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0008_vocabulary'),
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
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('correct', models.SmallIntegerField()),
                ('quantity', models.PositiveSmallIntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=255)),
                ('a', models.CharField(max_length=128)),
                ('b', models.CharField(max_length=128)),
                ('c', models.CharField(max_length=128)),
                ('d', models.CharField(max_length=128)),
                ('correct', models.CharField(choices=[('a', 'a'), ('b', 'b'), ('c', 'c'), ('d', 'd')], max_length=5)),
                ('test_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tests', to='user.testsection')),
            ],
        ),
        migrations.CreateModel(
            name='TestSectionResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='results', to='user.testsection')),
            ],
        ),
    ]
