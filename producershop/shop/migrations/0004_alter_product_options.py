# Generated by Django 4.1.7 on 2023-03-02 15:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_product_options_product_created_at'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-created_at']},
        ),
    ]
