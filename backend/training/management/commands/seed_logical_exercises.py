from django.core.management.base import BaseCommand
from training.models import Difficulty, Exercise, ExerciseType


class Command(BaseCommand):
    help = 'Creates the ten logical DuckyTraining exercises without educational content.'

    def handle(self, *args, **options):
        exercises = [
            (1, 'Secuencia de inicio', ExerciseType.ORDER_ALGORITHM, Difficulty.EASY, 'Secuenciación', 'Lógica general de DuckyWorld'),
            (2, 'Orden de una respuesta', ExerciseType.ORDER_ALGORITHM, Difficulty.EASY, 'Secuenciación', 'Práctica relacionada con QuizArenas'),
            (3, 'El error visible', ExerciseType.FIND_ERROR, Difficulty.EASY, 'Detección de errores', 'Práctica relacionada con DuckyClash'),
            (4, 'La opción correcta', ExerciseType.FIND_ERROR, Difficulty.MEDIUM, 'Lectura y decisión', 'Práctica relacionada con QuizArenas'),
            (5, 'Primera conexión', ExerciseType.CONNECT_NETWORK, Difficulty.MEDIUM, 'Relaciones entre componentes', 'Práctica relacionada con DuckyEscape'),
            (6, 'Ruta sin interrupciones', ExerciseType.CONNECT_NETWORK, Difficulty.MEDIUM, 'Diseño de conexiones', 'Práctica de infraestructura'),
            (7, 'Corrige antes de competir', ExerciseType.FIND_ERROR, Difficulty.MEDIUM, 'Validación', 'Práctica relacionada con DuckyClash'),
            (8, 'Ordena la estrategia', ExerciseType.ORDER_ALGORITHM, Difficulty.HARD, 'Planificación', 'Práctica relacionada con DuckyEscape'),
            (9, 'Red de salida', ExerciseType.CONNECT_NETWORK, Difficulty.HARD, 'Resolución de problemas', 'Práctica relacionada con DuckyEscape'),
            (10, 'Reto de preparación DuckyWorld', None, Difficulty.HARD, 'Integración de habilidad', 'Cierre de secuencia Pro'),
        ]
        for number, name, kind, difficulty, skill, relation in exercises:
            Exercise.objects.update_or_create(
                number=number,
                defaults={
                    'logical_name': name,
                    'exercise_type': kind,
                    'difficulty': difficulty,
                    'skill': skill,
                    'introductory_relation': relation,
                    'active': True,
                },
            )
        self.stdout.write(self.style.SUCCESS('10 logical DuckyTraining exercises created/updated.'))
