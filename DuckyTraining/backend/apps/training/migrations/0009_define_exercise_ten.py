from django.db import migrations


def set_exercise_ten_format(apps, schema_editor):
    Exercise = apps.get_model('training', 'Exercise')
    Exercise.objects.filter(number=10).update(
        logical_name='Encuentra el fallo',
        exercise_type='FIND_ERROR',
        skill='Detección de errores',
        introductory_relation='Cierre de secuencia',
    )


class Migration(migrations.Migration):
    dependencies = [
        ('training', '0008_training_access_xp_state'),
    ]

    operations = [
        migrations.RunPython(
            set_exercise_ten_format,
            migrations.RunPython.noop,
        ),
    ]
