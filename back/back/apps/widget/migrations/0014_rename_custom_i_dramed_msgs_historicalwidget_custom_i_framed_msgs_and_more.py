# Generated by Django 4.1.13 on 2024-10-07 19:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("widget", "0013_alter_historicalwidget_chatfaq_api_and_more"),
    ]

    operations = [
        migrations.RenameField(
            model_name="historicalwidget",
            old_name="custom_i_dramed_msgs",
            new_name="custom_i_framed_msgs",
        ),
        migrations.RenameField(
            model_name="widget",
            old_name="custom_i_dramed_msgs",
            new_name="custom_i_framed_msgs",
        ),
    ]
