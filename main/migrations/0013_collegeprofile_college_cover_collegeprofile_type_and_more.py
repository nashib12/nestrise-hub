# Generated by Django 5.1.4 on 2025-01-19 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_collegeinfo_course_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='collegeprofile',
            name='college_cover',
            field=models.ImageField(blank=True, upload_to='college profle cover'),
        ),
        migrations.AddField(
            model_name='collegeprofile',
            name='type',
            field=models.CharField(choices=[('Private', 'Private'), ('Government', 'Govenment')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='cover_image',
            field=models.ImageField(blank=True, upload_to='student cover img'),
        ),
    ]
