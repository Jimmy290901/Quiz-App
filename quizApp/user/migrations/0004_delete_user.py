# Generated by Django 3.2.4 on 2021-06-24 19:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_user_password'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]
