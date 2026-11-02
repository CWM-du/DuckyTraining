from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('training', '0002_alter_trainingattempt_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='difficulty',
            field=models.CharField(
                choices=[('EASY', 'Fácil'), ('MEDIUM', 'Media'), ('HARD', 'Difícil'), ('EXPERT', 'Experto')],
                max_length=16,
            ),
        ),
    ]
