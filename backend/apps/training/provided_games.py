"""Server-side practice for the three supplied, explicitly provisional datasets."""
import json
import random
from functools import lru_cache
from pathlib import Path


CONTENT_DIR = Path(__file__).resolve().parent / 'content'
GAME_FILES = {
    'asociar_conceptos': 'asociar_conceptos (1).json',
    'detectar_error': 'detectar_error.json',
    'ordenar_codigo': 'ordenar_codigo (1).json',
}
GAME_LABELS = {
    'asociar_conceptos': 'Asociar conceptos',
    'detectar_error': 'Detectar error',
    'ordenar_codigo': 'Ordenar código',
}


class ProvidedGameError(ValueError):
    """A supplied dataset or practice request is invalid."""


class ProvidedGameRequestError(ProvidedGameError):
    """A practice request refers to an invalid level, exercise, or answer shape."""


@lru_cache(maxsize=len(GAME_FILES))
def _load_game(game_id):
    filename = GAME_FILES.get(game_id)
    if filename is None:
        raise ProvidedGameError('El juego de práctica solicitado no existe.')

    try:
        with (CONTENT_DIR / filename).open('r', encoding='utf-8') as stream:
            data = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise ProvidedGameError('No se pudo leer el contenido del juego de práctica.') from exc

    if not isinstance(data, dict) or data.get('tipo_juego') != game_id:
        raise ProvidedGameError('El tipo del dataset no coincide con el juego solicitado.')
    if not isinstance(data.get('instrucciones'), str) or not data['instrucciones'].strip():
        raise ProvidedGameError('El dataset necesita instrucciones no vacías.')
    levels = data.get('niveles')
    if not isinstance(levels, list) or not levels:
        raise ProvidedGameError('El dataset debe contener niveles.')

    seen_levels = set()
    seen_exercise_ids = set()
    for level in levels:
        if not isinstance(level, dict):
            raise ProvidedGameError('El nivel debe ser un objeto JSON.')
        level_number = level.get('nivel')
        exercises = level.get('pruebas')
        if (not isinstance(level_number, int) or isinstance(level_number, bool)
                or level_number < 1 or level_number in seen_levels
                or not isinstance(exercises, list) or not exercises):
            raise ProvidedGameError('El nivel tiene una estructura o identificador inválido.')
        seen_levels.add(level_number)
        for exercise in exercises:
            if not isinstance(exercise, dict):
                raise ProvidedGameError('La prueba debe ser un objeto JSON.')
            exercise_id = exercise.get('id')
            if (not isinstance(exercise_id, str) or not exercise_id.strip()
                    or exercise_id in seen_exercise_ids or exercise.get('nivel') != level_number):
                raise ProvidedGameError('La prueba tiene un identificador o nivel inválido.')
            seen_exercise_ids.add(exercise_id)
            _validate_exercise(game_id, exercise)
    return data


def _validate_exercise(game_id, exercise):
    if game_id == 'asociar_conceptos':
        concepts = exercise.get('conceptos')
        explanations = exercise.get('explicaciones')
        associations = exercise.get('asociaciones')
        if not _valid_items(concepts) or not _valid_items(explanations):
            raise ProvidedGameError('La prueba de asociación necesita conceptos y explicaciones válidos.')
        concept_ids = [item['id'] for item in concepts]
        explanation_ids = [item['id'] for item in explanations]
        if (len(concept_ids) != len(set(concept_ids))
                or len(explanation_ids) != len(set(explanation_ids))
                or len({item['texto'] for item in concepts}) != len(concepts)
                or len({item['texto'] for item in explanations}) != len(explanations)
                or not isinstance(associations, list)
                or len(associations) != len(concept_ids)):
            raise ProvidedGameError('La prueba de asociación contiene identificadores o parejas inválidos.')
        if not all(
            isinstance(pair, dict)
            and pair.get('concepto_id') in concept_ids
            and pair.get('explicacion_id') in explanation_ids
            for pair in associations
        ):
            raise ProvidedGameError('Una asociación referencia elementos inexistentes.')
        if (len({pair['concepto_id'] for pair in associations}) != len(associations)
                or len({pair['explicacion_id'] for pair in associations}) != len(associations)):
            raise ProvidedGameError('Cada concepto y explicación debe aparecer una sola vez.')
    elif game_id == 'detectar_error':
        code = exercise.get('codigo')
        if (not isinstance(code, list) or not code
                or not all(isinstance(item, dict)
                           and isinstance(item.get('linea'), str)
                           and type(item.get('error')) is bool for item in code)
                or len({item['linea'] for item in code}) != len(code)
                or sum(item['error'] is True for item in code) != 1):
            raise ProvidedGameError('Cada prueba debe contener líneas únicas y exactamente una línea errónea.')
    elif game_id == 'ordenar_codigo':
        blocks = exercise.get('bloques')
        correct_order = exercise.get('orden_correcto')
        if (not isinstance(blocks, list) or not blocks
                or not all(isinstance(item, dict)
                           and isinstance(item.get('id'), str) and item['id'].strip()
                           and isinstance(item.get('linea'), str) for item in blocks)):
            raise ProvidedGameError('La prueba debe contener bloques con identificador y línea.')
        block_ids = [item['id'] for item in blocks]
        if (len(block_ids) != len(set(block_ids))
                or not isinstance(correct_order, list) or not correct_order
                or not all(isinstance(item, str) for item in correct_order)
                or len(correct_order) != len(set(correct_order))
                or set(correct_order) != set(block_ids)):
            raise ProvidedGameError('El orden correcto debe contener cada ID de bloque una sola vez.')


def _valid_items(items):
    return (
        isinstance(items, list) and bool(items)
        and all(isinstance(item, dict)
                and isinstance(item.get('id'), str) and item['id'].strip()
                and isinstance(item.get('texto'), str) and item['texto'].strip()
                for item in items)
    )


def list_games():
    games = []
    for game_id in GAME_FILES:
        data = _load_game(game_id)
        games.append({
            'id': game_id,
            'name': GAME_LABELS[game_id],
            'instruction': data['instrucciones'],
            'levels': sorted(level['nivel'] for level in data['niveles']),
            'content_status': 'provisional',
        })
    return games


def get_random_challenge(game_id, level_number):
    if game_id not in GAME_FILES:
        raise ProvidedGameRequestError('El juego de práctica solicitado no existe.')
    data = _load_game(game_id)
    if not isinstance(level_number, int) or isinstance(level_number, bool):
        raise ProvidedGameRequestError('El nivel debe ser un entero.')
    matching_levels = [level for level in data['niveles'] if level['nivel'] == level_number]
    if not matching_levels:
        raise ProvidedGameRequestError('El nivel solicitado no existe en este juego.')
    exercise = random.choice(matching_levels[0]['pruebas'])
    if game_id == 'asociar_conceptos':
        concepts = [item['texto'] for item in exercise['conceptos']]
        explanations = [item['texto'] for item in exercise['explicaciones']]
        random.shuffle(concepts)
        random.shuffle(explanations)
        content = {'conceptos': concepts, 'explicaciones': explanations}
    elif game_id == 'detectar_error':
        lines = [{'linea': item['linea']} for item in exercise['codigo']]
        random.shuffle(lines)
        content = {'codigo': lines}
    else:
        blocks = list(exercise['bloques'])
        random.shuffle(blocks)
        content = {'bloques': blocks}
    return {
        'game': {
            'id': game_id,
            'name': GAME_LABELS[game_id],
            'instruction': data['instrucciones'],
            'content_status': 'provisional',
        },
        'exercise_id': exercise['id'],
        'level': level_number,
        'content': content,
    }


def validate_answer(game_id, exercise_id, answer, level_number):
    if game_id not in GAME_FILES:
        raise ProvidedGameRequestError('El juego de práctica solicitado no existe.')
    data = _load_game(game_id)
    if not isinstance(exercise_id, str) or not isinstance(answer, dict) or not answer:
        raise ProvidedGameRequestError('Se requiere un identificador de prueba y una respuesta JSON.')

    exercise = next(
        (item for level in data['niveles'] for item in level['pruebas']
         if item['id'] == exercise_id),
        None,
    )
    if exercise is None:
        raise ProvidedGameRequestError('La prueba indicada no existe en este juego.')
    if exercise['nivel'] != level_number:
        raise ProvidedGameRequestError('La prueba no corresponde al nivel indicado.')

    if game_id == 'asociar_conceptos':
        submitted = answer.get('asociaciones')
        correct = _validate_associations(exercise, submitted)
        solution = {
            'asociaciones': [
                {'concepto': concept, 'explicacion': explanation}
                for concept, explanation in _association_text_pairs(exercise)
            ]
        }
    elif game_id == 'detectar_error':
        selected_line = answer.get('selected_line')
        matching_lines = [
            item for item in exercise['codigo']
            if item['linea'] == selected_line
        ] if isinstance(selected_line, str) else []
        correct = (
            len(matching_lines) == 1 and matching_lines[0]['error'] is True
        )
        solution = {'selected_line': next(item['linea'] for item in exercise['codigo'] if item['error'] is True)}
    else:
        submitted = answer.get('ordered_ids')
        correct = (
            isinstance(submitted, list)
            and all(isinstance(item, str) for item in submitted)
            and submitted == exercise['orden_correcto']
        )
        solution = {'ordered_ids': exercise['orden_correcto']}

    result = {'correct': correct, 'solution': solution}
    explanation = exercise.get('explicacion')
    if isinstance(explanation, str) and explanation.strip():
        result['explanation'] = explanation
    return result


def _validate_associations(exercise, submitted):
    if not isinstance(submitted, list) or not submitted:
        return False
    if not all(
        isinstance(pair, dict)
        and isinstance(pair.get('concepto'), str)
        and isinstance(pair.get('explicacion'), str)
        for pair in submitted
    ):
        return False
    if (len({pair['concepto'] for pair in submitted}) != len(submitted)
            or len({pair['explicacion'] for pair in submitted}) != len(submitted)):
        return False
    expected = set(_association_text_pairs(exercise))
    return len(submitted) == len(expected) and {
        (pair['concepto'], pair['explicacion']) for pair in submitted
    } == expected


def _association_text_pairs(exercise):
    concept_text = {item['id']: item['texto'] for item in exercise['conceptos']}
    explanation_text = {item['id']: item['texto'] for item in exercise['explicaciones']}
    return [
        (concept_text[pair['concepto_id']], explanation_text[pair['explicacion_id']])
        for pair in exercise['asociaciones']
    ]
