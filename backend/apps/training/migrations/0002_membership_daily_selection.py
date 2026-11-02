from django.db import migrations, models
import django.db.models.deletion


def migrate_legacy_memberships(apps, schema_editor):
    UserTrainingProfile = apps.get_model('training', 'UserTrainingProfile')
    DailyCycle = apps.get_model('training', 'DailyCycle')
    UserTrainingProfile.objects.filter(membership='ALUMNO_PLUS_TEMPORAL').update(membership='PLUS')
    DailyCycle.objects.filter(effective_membership='ALUMNO_PLUS_TEMPORAL').update(effective_membership='PLUS')


class Migration(migrations.Migration):
    dependencies = [('training', '0001_initial')]

    operations = [
        migrations.RenameField(
            model_name='usertrainingprofile',
            old_name='access_level',
            new_name='membership',
        ),
        migrations.AlterField(
            model_name='usertrainingprofile',
            name='membership',
            field=models.CharField(
                choices=[('FREE', 'Free'), ('PLUS', 'Plus'), ('PRO', 'Pro')],
                default='FREE',
                help_text='Temporal: será reemplazado por el contrato oficial de Equipo 0/Ecomotor.',
                max_length=16,
            ),
        ),
        migrations.RenameField(
            model_name='dailycycle',
            old_name='effective_access_level',
            new_name='effective_membership',
        ),
        migrations.RunPython(migrate_legacy_memberships, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='dailycycle',
            name='effective_membership',
            field=models.CharField(
                choices=[('FREE', 'Free'), ('PLUS', 'Plus'), ('PRO', 'Pro')],
                max_length=16,
            ),
        ),
        migrations.AddField(
            model_name='dailycycle',
            name='daily_selection_size',
            field=models.PositiveSmallIntegerField(default=3),
        ),
        migrations.RemoveField(model_name='dailycycle', name='final_reward_processed'),
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
        migrations.AddField(
            model_name='trainingattempt',
            name='xp_reward_processed',
            field=models.BooleanField(default=False, help_text='XP de esta partida: se procesa por intento correcto según contrato del Ecomotor.'),
        ),
    ]
