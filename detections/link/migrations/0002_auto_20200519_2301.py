# Generated by Django 3.0.5 on 2020-05-19 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('link', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='link',
            name='detection',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='link',
            name='keywords',
            field=models.TextField(null=True),
        ),
    ]
