# Generated by Django 5.0.1 on 2024-03-13 04:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("top_products", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="best_sellers_list",
            old_name="web_link",
            new_name="link",
        ),
    ]
