# Generated by Django 5.1 on 2024-12-10 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0004_rename_address1_ordermodel_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='couponmodel',
            name='code',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
