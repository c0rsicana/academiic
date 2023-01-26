# Generated by Django 3.2.5 on 2022-12-21 06:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Students',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LRN', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12, 'Learner Reference Number must be a 12 Digit Number')])),
                ('first_Name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'First Name must be greater than 1 Character')])),
                ('middle_Name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Middle Name must be greater than 1 Character')])),
                ('last_Name', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2, 'Last Name must be greater than 1 Character')])),
                ('suffix_Name', models.CharField(max_length=10, validators=[django.core.validators.MinLengthValidator(2, 'Suffix Name must be greater than 1 Character')])),
                ('address', models.CharField(max_length=255)),
                ('birthdate', models.DateField(null=True)),
                ('admission_Date', models.DateField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('gender', models.CharField(choices=[('MALE', 'MALE'), ('FEMALE', 'FEMALE')], max_length=10)),
                ('status', models.CharField(choices=[('ENROLLED', 'ENROLLED'), ('TRANSFERRED', 'TRANSFERRED'), ('LEAVER', 'LEAVER'), ('DROPPED', 'DROPPED')], default='ENROLLED', max_length=15)),
                ('slug', models.SlugField(unique=True)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.level')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='management.section')),
            ],
            options={
                'ordering': ['level'],
            },
        ),
    ]