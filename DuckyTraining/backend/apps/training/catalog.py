"""Carga y valida el catálogo educativo JSON de DuckyTraining.

El catálogo inicial solo contiene plantillas pendientes. No se generan preguntas
ni soluciones automáticamente: una variante solo puede usarse cuando su estado
es ``published`` y su contenido supera la validación del formato.
"""
from __future__ import annotations

import json
import random
from functools import lru_cache
from pathlib import Path

from .models import ExerciseType

CATALOG_PATH = Path(__file__).resolve().parent / 'content' / 'catalog.json'


class CatalogError(ValueError):
    """El catálogo o una variante publicada no cumple el contrato esperado."""


@lru_cache(maxsize=1)
def _read_catalog_cached():
    try:
        with CATALOG_PATH.open('r', encoding='utf-8') as stream:
            catalog = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise CatalogError('No se pudo leer el catálogo educativo JSON.') from exc
    if not isinstance(catalog, dict) or catalog.get('schema_version') != 1:
        raise CatalogError('Versión o estructura raíz del catálogo no válida.')
    exercises = catalog.get('exercises')
    if not isinstance(exercises, list):
        raise CatalogError("El catálogo debe contener una lista 'exercises'.")
    return catalog


def clear_catalog_cache():
    """Vacía la caché; útil después de sustituir el JSON durante desarrollo."""
    _read_catalog_cached.cache_clear()


def get_catalog():
    return _read_catalog_cached()


def _exercise_entry(exercise_number):
    matches = [entry for entry in get_catalog()['exercises']
               if isinstance(entry, dict) and entry.get('exercise_number') == exercise_number]
    if len(matches) != 1:
        raise CatalogError(f'El catálogo debe definir exactamente una entrada para el juego {exercise_number}.')
    return matches[0]


def validate_variant_content(exercise_type, content):
    """Valida la estructura mínima de contenido, no la calidad pedagógica."""
    if not isinstance(content, dict):
        raise CatalogError('El contenido de la variante debe ser un objeto JSON.')
    if not isinstance(content.get('instruction'), str) or not content['instruction'].strip():
        raise CatalogError("La variante necesita una instrucción no vacía ('instruction').")
    if not isinstance(content.get('explanation'), str) or not content['explanation'].strip():
        raise CatalogError("La variante necesita una explicación no vacía ('explanation').")

    if exercise_type == ExerciseType.ORDER_ALGORITHM:
        steps, expected = content.get('steps'), content.get('expected_order')
        if not isinstance(steps, list) or not steps or not all(
            isinstance(item, dict) and isinstance(item.get('id'), str) and item['id']
            and isinstance(item.get('text'), str) and item['text'].strip() for item in steps
        ):
            raise CatalogError("'steps' debe ser una lista de objetos con 'id' y 'text'.")
        ids = [item['id'] for item in steps]
        if len(ids) != len(set(ids)):
            raise CatalogError("Los identificadores de 'steps' deben ser únicos.")
        if not isinstance(expected, list) or expected != ids:
            raise CatalogError("'expected_order' debe contener los identificadores de los pasos en el orden correcto.")
    elif exercise_type == ExerciseType.FIND_ERROR:
        code_items, expected = content.get('code_items'), content.get('expected_bug_id')
        if not isinstance(code_items, list) or not code_items or not all(
            isinstance(item, dict) and isinstance(item.get('id'), str) and item['id']
            and isinstance(item.get('text'), str) and item['text'].strip() for item in code_items
        ):
            raise CatalogError("'code_items' debe ser una lista de objetos con 'id' y 'text'.")
        ids = [item['id'] for item in code_items]
        if len(ids) != len(set(ids)):
            raise CatalogError("Los identificadores de 'code_items' deben ser únicos.")
        if not isinstance(expected, str) or expected not in ids:
            raise CatalogError("'expected_bug_id' debe coincidir con un identificador de 'code_items'.")
    elif exercise_type == ExerciseType.CONNECT_NETWORK:
        nodes, expected = content.get('nodes'), content.get('expected_connections')
        if not isinstance(nodes, list) or len(nodes) < 2 or not all(
            isinstance(item, dict) and isinstance(item.get('id'), str) and item['id']
            and isinstance(item.get('label'), str) and item['label'].strip() for item in nodes
        ):
            raise CatalogError("'nodes' debe contener al menos dos objetos con 'id' y 'label'.")
        ids = [item['id'] for item in nodes]
        if len(ids) != len(set(ids)):
            raise CatalogError("Los identificadores de 'nodes' deben ser únicos.")
        if not isinstance(expected, list) or not expected:
            raise CatalogError("'expected_connections' debe ser una lista no vacía.")
        normalized = []
        for connection in expected:
            if (not isinstance(connection, list) or len(connection) != 2
                    or not all(isinstance(node_id, str) and node_id in ids for node_id in connection)
                    or connection[0] == connection[1]):
                raise CatalogError("Cada conexión esperada debe enlazar dos nodos distintos existentes.")
            pair = tuple(sorted(connection))
            if pair in normalized:
                raise CatalogError("'expected_connections' no puede contener conexiones duplicadas.")
            normalized.append(pair)
    else:
        raise CatalogError(f'Tipo de ejercicio no soportado: {exercise_type}.')
    return content


def get_variant(variant_key, expected_exercise_number=None, expected_type=None):
    """Devuelve contenido publicado validado; None si la variante está pendiente."""
    for entry in get_catalog()['exercises']:
        if not isinstance(entry, dict):
            continue
        for variant in entry.get('variants', []):
            if isinstance(variant, dict) and variant.get('variant_key') == variant_key:
                if expected_exercise_number is not None and entry.get('exercise_number') != expected_exercise_number:
                    raise CatalogError('La variante asignada no corresponde a este juego.')
                if expected_type is not None and entry.get('exercise_type') != expected_type:
                    raise CatalogError('El formato de la variante no coincide con el juego.')
                if variant.get('status') != 'published' or variant.get('content') is None:
                    return None
                content = validate_variant_content(entry.get('exercise_type'), variant.get('content'))
                return {'variant_key': variant_key, 'exercise_number': entry['exercise_number'],
                        'exercise_type': entry['exercise_type'], **content}
    raise CatalogError(f'La clave de variante {variant_key!r} no existe en el catálogo.')


def choose_published_variant(exercise_number, exercise_type):
    """Elige una variante publicada; no crea ni inventa contenido educativo."""
    entry = _exercise_entry(exercise_number)
    if entry.get('exercise_type') != exercise_type:
        raise CatalogError('El tipo del juego no coincide con el catálogo.')
    published = []
    for variant in entry.get('variants', []):
        if not isinstance(variant, dict) or variant.get('status') != 'published':
            continue
        content = validate_variant_content(exercise_type, variant.get('content'))
        published.append((variant.get('variant_key'), content))
    if not published:
        return None
    key, content = random.choice(published)
    return key, {'variant_key': key, 'exercise_number': exercise_number,
                 'exercise_type': exercise_type, **content}


def get_or_assign_monthly_variant(user, exercise, month):
    """Recupera o asigna una variante publicada estable para usuario/juego/mes.

    Devuelve (asignación, contenido). Si aún no hay contenido publicado devuelve
    (None, None), sin fabricar preguntas ni crear asignaciones ficticias.
    """
    from django.db import IntegrityError, transaction
    from .models import MonthlyVariantAssignment

    assignment = MonthlyVariantAssignment.objects.filter(
        user=user, exercise=exercise, month=month
    ).first()
    if assignment:
        return assignment, get_variant(
            assignment.variant_key,
            expected_exercise_number=exercise.number,
            expected_type=exercise.exercise_type,
        )

    selected = choose_published_variant(exercise.number, exercise.exercise_type)
    if selected is None:
        return None, None
    variant_key, content = selected
    try:
        with transaction.atomic():
            assignment, created = MonthlyVariantAssignment.objects.get_or_create(
                user=user, exercise=exercise, month=month,
                defaults={'variant_key': variant_key},
            )
        if not created:
            content = get_variant(
                assignment.variant_key,
                expected_exercise_number=exercise.number,
                expected_type=exercise.exercise_type,
            )
        return assignment, content
    except IntegrityError:
        # Una solicitud concurrente pudo crear la asignación primero.
        assignment = MonthlyVariantAssignment.objects.get(
            user=user, exercise=exercise, month=month
        )
        return assignment, get_variant(
            assignment.variant_key,
            expected_exercise_number=exercise.number,
            expected_type=exercise.exercise_type,
        )
