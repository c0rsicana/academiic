# Generated by Django 3.2.5 on 2023-01-13 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0005_remove_students_overall_average'),
    ]

    operations = [
        migrations.AddField(
            model_name='students',
            name='overall_average',
            field=models.FloatField(default=0),
        ),
    ]