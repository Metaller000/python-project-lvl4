# Generated by Django 3.2.3 on 2021-06-11 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210611_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='description',
            field=models.CharField(default=' ', max_length=500),
            preserve_default=False,
        ),
    ]