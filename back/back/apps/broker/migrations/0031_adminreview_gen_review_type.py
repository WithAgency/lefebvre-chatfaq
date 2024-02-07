# Generated by Django 4.1.13 on 2024-01-05 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("broker", "0030_rename_review_adminreview_gen_review_msg_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="adminreview",
            name="gen_review_type",
            field=models.CharField(
                blank=True,
                choices=[
                    ("alternative_answer", "Alternative Answer"),
                    ("review", "Review"),
                ],
                max_length=255,
                null=True,
            ),
        ),
    ]
