# Generated by Django 3.2.5 on 2023-01-12 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('management', '0002_announcement'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='date_expired',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='announcement',
            name='created_at',
            field=models.DateTimeField(),
        ),
    ]
