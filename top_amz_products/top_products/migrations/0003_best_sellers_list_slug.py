# Generated by Django 5.0.1 on 2024-04-29 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("top_products", "0002_rename_web_link_best_sellers_list_link"),
    ]

    operations = [
        migrations.AddField(
            model_name="best_sellers_list",
            name="slug",
            field=models.SlugField(default="", null=True),
        ),
    ]
