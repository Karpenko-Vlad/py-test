# Generated by Django 3.0.7 on 2020-06-13 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_carditem_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='invoice',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
