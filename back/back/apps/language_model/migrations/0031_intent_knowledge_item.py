# Generated by Django 4.1.12 on 2023-10-31 17:42

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("language_model", "0030_intent_knowledge_base"),
    ]

    operations = [
        migrations.AddField(
            model_name="intent",
            name="knowledge_item",
            field=models.ManyToManyField(blank=True, to="language_model.knowledgeitem"),
        ),
    ]
