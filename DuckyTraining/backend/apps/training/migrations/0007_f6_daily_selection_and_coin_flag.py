from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('training', '0006_remove_trainingattempt_xp_reward_processed'),
    ]

    operations = [
        migrations.AddField(
            model_name='dailycycle',
            name='selected_exercises',
            field=models.ManyToManyField(blank=True, related_name='daily_cycles', to='training.exercise'),
        ),
        migrations.RenameField(
            model_name='dailyexerciseprogress',
            old_name='xp_reward_processed',
            new_name='ducky_coin_reward_processed',
        ),
    ]
