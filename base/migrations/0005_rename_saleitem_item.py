# Generated by Django 4.1.7 on 2023-03-20 04:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_rename_item_saleitem'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='SaleItem',
            new_name='Item',
        ),
    ]
