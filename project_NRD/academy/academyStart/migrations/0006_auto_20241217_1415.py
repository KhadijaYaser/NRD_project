# Generated by Django 3.1.12 on 2024-12-17 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('academyStart', '0005_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='status',
            field=models.CharField(choices=[('open', 'Open for Registration'), ('close', 'Closed')], default='close', max_length=20),
        ),
    ]
