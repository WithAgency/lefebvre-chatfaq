# Generated by Django 4.1.4 on 2022-12-22 10:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("broker", "0004_rename_fsm_platformbot_fsm_def"),
        ("fsm", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="CachedMachine",
            new_name="CachedFSM",
        ),
        migrations.RenameModel(
            old_name="FiniteStateMachine",
            new_name="FSMDefinition",
        ),
        migrations.RenameField(
            model_name="cachedfsm",
            old_name="fsm",
            new_name="fsm_def",
        ),
    ]
