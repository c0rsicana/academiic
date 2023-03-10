# Generated by Django 3.2.5 on 2022-12-21 06:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('management', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('academic_Year', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='management.academicyear')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('section', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='subject_section', to='management.section')),
            ],
            options={
                'ordering': ['section'],
                'unique_together': {('section', 'name', 'academic_Year')},
            },
        ),
    ]
