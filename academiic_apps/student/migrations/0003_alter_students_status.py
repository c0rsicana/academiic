# Generated by Django 3.2.5 on 2023-01-13 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0002_alter_students_suffix_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='status',
            field=models.CharField(choices=[('ENROLLED', 'ENROLLED'), ('TRANSFERRED', 'TRANSFERRED'), ('GRADUATED', 'GRADUATED'), ('LEAVER', 'LEAVER'), ('DROPPED', 'DROPPED')], default='ENROLLED', max_length=15),
        ),
    ]
