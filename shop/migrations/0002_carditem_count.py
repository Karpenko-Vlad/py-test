# Generated by Django 3.0.7 on 2020-06-13 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='carditem',
            name='count',
            field=models.IntegerField(default=0),
        ),
    ]
