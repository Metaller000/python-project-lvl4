# Generated by Django 3.2.3 on 2021-06-11 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_tasks_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]