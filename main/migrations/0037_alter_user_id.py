# Generated by Django 4.1.2 on 2022-11-19 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]