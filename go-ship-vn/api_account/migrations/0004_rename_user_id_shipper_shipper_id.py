# Generated by Django 3.2 on 2022-11-09 08:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api_account', '0003_auto_20221109_0106'),
    ]

    operations = [
        migrations.RenameField(
            model_name='shipper',
            old_name='user_id',
            new_name='shipper_id',
        ),
    ]