# Generated by Django 4.1.2 on 2022-11-14 21:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0035_alter_user_auth0_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigIntegerField(primary_key=True, serialize=False),
        ),
    ]