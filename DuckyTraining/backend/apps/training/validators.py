"""Validadores server-side para los tres formatos de DuckyTraining."""


def _explanation(variant_data, fallback):
    text = variant_data.get('explanation') if isinstance(variant_data, dict) else None
    return text.strip() if isinstance(text, str) and text.strip() else fallback


def validate_sorting(variant_data, user_answer):
    """Compara el orden recibido con la solución de la variante publicada."""
    if not isinstance(variant_data, dict) or not isinstance(user_answer, dict):
        return False, 'La respuesta enviada no tiene el formato esperado.'
    expected = variant_data.get('expected_order')
    submitted = user_answer.get('ordered_ids')
    if not isinstance(expected, list) or not expected:
        return False, 'La variante no tiene una solución de orden válida.'
    if not isinstance(submitted, list) or not all(isinstance(item, str) for item in submitted):
        return False, 'Envía una lista válida de identificadores ordenados.'
    if expected == submitted:
        return True, ''
    return False, _explanation(variant_data, 'El orden de los pasos no es correcto.')


def validate_bug_finding(variant_data, user_answer):
    """Comprueba el identificador del fallo seleccionado."""
    if not isinstance(variant_data, dict) or not isinstance(user_answer, dict):
        return False, 'La respuesta enviada no tiene el formato esperado.'
    expected = variant_data.get('expected_bug_id')
    submitted = user_answer.get('selected_bug_id')
    if not isinstance(expected, str) or not expected:
        return False, 'La variante no tiene un fallo esperado configurado.'
    if not isinstance(submitted, str) or not submitted:
        return False, 'Selecciona el identificador del fallo.'
    if expected == submitted:
        return True, ''
    return False, _explanation(variant_data, 'Ese no es el error principal.')


def validate_networking(variant_data, user_answer):
    """Compara conexiones sin importar el orden de pares ni la dirección."""
    if not isinstance(variant_data, dict) or not isinstance(user_answer, dict):
        return False, 'La respuesta enviada no tiene el formato esperado.'
    expected = variant_data.get('expected_connections')
    submitted = user_answer.get('connections')
    if not isinstance(expected, list) or not expected:
        return False, 'La variante no tiene conexiones esperadas configuradas.'
    if not isinstance(submitted, list):
        return False, 'Envía una lista válida de conexiones.'

    def normalize(connections):
        normalized = []
        for pair in connections:
            if (not isinstance(pair, list) or len(pair) != 2
                    or not all(isinstance(node_id, str) and node_id for node_id in pair)
                    or pair[0] == pair[1]):
                raise ValueError('Conexión mal formada')
            normalized.append(tuple(sorted(pair)))
        if len(normalized) != len(set(normalized)):
            raise ValueError('Conexiones duplicadas')
        return sorted(normalized)

    try:
        if normalize(expected) == normalize(submitted):
            return True, ''
    except (TypeError, ValueError):
        pass
    return False, _explanation(variant_data, 'Las conexiones de red no son correctas.')
