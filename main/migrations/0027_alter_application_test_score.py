# Generated by Django 5.1.4 on 2025-02-08 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0026_faqs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='test_score',
            field=models.CharField(max_length=100),
        ),
    ]
