# Generated by Django 4.1.7 on 2023-03-20 04:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_saleitem_item'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Item',
            new_name='SaleItem',
        ),
    ]
