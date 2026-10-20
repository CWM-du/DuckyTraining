from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('training', '0007_f6_daily_selection_and_coin_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='usertrainingprofile',
            name='access_expires_at',
            field=models.DateTimeField(
                blank=True,
                help_text='Caducidad del acceso temporal; debe definirse para activar Alumno Plus temporal.',
                null=True,
            ),
        ),
        migrations.AddField(
            model_name='dailyexerciseprogress',
            name='xp_reward_processed',
            field=models.BooleanField(default=False),
        ),
    ]
