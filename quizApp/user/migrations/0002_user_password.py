# Generated by Django 3.2.4 on 2021-06-24 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default=1234, max_length=100),
            preserve_default=False,
        ),
    ]
