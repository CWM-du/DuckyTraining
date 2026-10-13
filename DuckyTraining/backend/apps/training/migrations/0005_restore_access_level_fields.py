
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("training", "0004_merge_20261013_1101"),
    ]

    operations = [
        migrations.RenameField(
            model_name="usertrainingprofile",
            old_name="membership",
            new_name="access_level",
        ),
        migrations.AlterField(
            model_name="usertrainingprofile",
            name="access_level",
            field=models.CharField(
                choices=[
                    ("FREE", "Free"),
                    ("ALUMNO_PLUS_TEMPORAL", "Alumno con Plus temporal"),
                    ("PLUS", "Plus"),
                    ("PRO", "Pro"),
                ],
                default="FREE",
                max_length=32,
            ),
        ),
        migrations.RenameField(
            model_name="dailycycle",
            old_name="effective_membership",
            new_name="effective_access_level",
        ),
        migrations.AlterField(
            model_name="dailycycle",
            name="effective_access_level",
            field=models.CharField(
                choices=[
                    ("FREE", "Free"),
                    ("ALUMNO_PLUS_TEMPORAL", "Alumno con Plus temporal"),
                    ("PLUS", "Plus"),
                    ("PRO", "Pro"),
                ],
                max_length=32,
            ),
        ),
        migrations.AddField(
            model_name="dailycycle",
            name="final_reward_processed",
            field=models.BooleanField(default=False),
        ),
        migrations.RenameField(
            model_name="dailyexerciseprogress",
            old_name="ducky_coin_reward_processed",
            new_name="xp_reward_processed",
        ),
        migrations.RemoveField(
            model_name="dailycycle",
            name="daily_selection_size",
        ),
        migrations.RemoveField(
            model_name="dailycycle",
            name="selected_exercises",
        ),
    ]