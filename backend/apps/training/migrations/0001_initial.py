from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]
    operations = [
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.PositiveSmallIntegerField(unique=True)),
                ('logical_name', models.CharField(max_length=150)),
                ('exercise_type', models.CharField(blank=True, choices=[('ORDER_ALGORITHM', 'Ordena el algoritmo'), ('FIND_ERROR', 'Encuentra el fallo'), ('CONNECT_NETWORK', 'Conecta la red')], max_length=32, null=True)),
                ('difficulty', models.CharField(choices=[('EASY', 'Fácil'), ('MEDIUM', 'Media'), ('HARD', 'Difícil')], max_length=16)),
                ('skill', models.CharField(max_length=120)),
                ('introductory_relation', models.CharField(max_length=180)),
                ('active', models.BooleanField(default=True)),
            ],
            options={'ordering': ['number']},
        ),
        migrations.CreateModel(
            name='UserTrainingProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('access_level', models.CharField(choices=[('FREE', 'Free'), ('ALUMNO_PLUS_TEMPORAL', 'Alumno con Plus temporal'), ('PLUS', 'Plus'), ('PRO', 'Pro')], default='FREE', max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyCycle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cycle_date', models.DateField()),
                ('effective_access_level', models.CharField(choices=[('FREE', 'Free'), ('ALUMNO_PLUS_TEMPORAL', 'Alumno con Plus temporal'), ('PLUS', 'Plus'), ('PRO', 'Pro')], max_length=32)),
                ('daily_limit', models.PositiveSmallIntegerField()),
                ('completed_count', models.PositiveSmallIntegerField(default=0)),
                ('final_reward_processed', models.BooleanField(default=False)),
                ('streak_processed', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='MonthlyVariantAssignment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.DateField(help_text='Primer día del mes de asignación')),
                ('variant_key', models.CharField(max_length=100)),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyExerciseProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed', models.BooleanField(default=False)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
                ('xp_reward_processed', models.BooleanField(default=False)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_progress', to='training.dailycycle')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingAttempt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('answer_payload', models.JSONField()),
                ('is_correct', models.BooleanField()),
                ('error_explanation', models.TextField(blank=True)),
                ('cycle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.dailycycle')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='training.exercise')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SkillProgress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=120)),
                ('successful_completions', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingStreak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_streak', models.PositiveIntegerField(default=0)),
                ('last_completion_date', models.DateField(blank=True, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingAchievement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('achievement_key', models.CharField(max_length=100)),
                ('granted_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(model_name='dailycycle', constraint=models.UniqueConstraint(fields=('user', 'cycle_date'), name='unique_training_daily_cycle')),
        migrations.AddConstraint(model_name='dailyexerciseprogress', constraint=models.UniqueConstraint(fields=('cycle', 'exercise'), name='unique_training_daily_exercise')),
        migrations.AddConstraint(model_name='monthlyvariantassignment', constraint=models.UniqueConstraint(fields=('user', 'exercise', 'month'), name='unique_training_month_variant')),
        migrations.AddConstraint(model_name='skillprogress', constraint=models.UniqueConstraint(fields=('user', 'skill'), name='unique_training_skill_progress')),
        migrations.AddConstraint(model_name='trainingachievement', constraint=models.UniqueConstraint(fields=('user', 'achievement_key'), name='unique_training_achievement')),
    ]
