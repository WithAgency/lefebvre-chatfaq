# Generated by Django 4.2.17 on 2024-12-10 14:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broker', '0041_message_file_request_message_upload_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='file_request',
        ),
        migrations.RemoveField(
            model_name='message',
            name='upload_path',
        ),
    ]
