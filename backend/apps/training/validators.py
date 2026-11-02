"""Validadores puros. La estructura del contenido se valida antes en catalog.py."""


def _error_message(variant_data, fallback):
    message = variant_data.get('error_explanation')
    return message if isinstance(message, str) and message.strip() else fallback


def validate_sorting(variant_data, user_answer):
    """Valida 'Ordena el algoritmo'; un contenido vacío o inconsistente falla cerrado."""
    expected_order = variant_data.get('expected_order')
    user_order = user_answer.get('ordered_ids') if isinstance(user_answer, dict) else None
    if (not isinstance(expected_order, list) or not expected_order
            or not all(isinstance(item, str) and item for item in expected_order)
            or len(expected_order) != len(set(expected_order))):
        return False, 'La variante de ordenación no contiene una solución válida.'
    if not isinstance(user_order, list) or not user_order or not all(isinstance(item, str) for item in user_order):
        return False, _error_message(variant_data, 'Envía una lista de pasos válida.')
    if expected_order == user_order:
        return True, ''
    return False, _error_message(variant_data, 'El orden de los pasos no es correcto.')


def validate_bug_finding(variant_data, user_answer):
    """Valida 'Encuentra el fallo' contra un identificador esperado no vacío."""
    expected_bug_id = variant_data.get('expected_bug_id')
    user_bug_id = user_answer.get('selected_bug_id') if isinstance(user_answer, dict) else None
    if not isinstance(expected_bug_id, str) or not expected_bug_id.strip():
        return False, 'La variante no contiene una solución válida.'
    if isinstance(user_bug_id, str) and expected_bug_id == user_bug_id:
        return True, ''
    return False, _error_message(variant_data, 'Ese no es el error principal.')


def validate_networking(variant_data, user_answer):
    """Compara conexiones no dirigidas y rechaza respuestas/contenidos vacíos."""
    expected_connections = variant_data.get('expected_connections')
    user_connections = user_answer.get('connections') if isinstance(user_answer, dict) else None
    if not isinstance(expected_connections, list) or not expected_connections:
        return False, 'La variante de red no contiene conexiones esperadas válidas.'
    if not isinstance(user_connections, list) or not user_connections:
        return False, _error_message(variant_data, 'Debes crear las conexiones requeridas.')

    def normalize(connections):
        result = []
        for connection in connections:
            if (not isinstance(connection, (list, tuple)) or len(connection) != 2
                    or not all(isinstance(node_id, str) and node_id for node_id in connection)
                    or connection[0] == connection[1]):
                raise ValueError('Conexión inválida')
            pair = tuple(sorted(connection))
            if pair in result:
                raise ValueError('Conexión duplicada')
            result.append(pair)
        return sorted(result)

    try:
        expected_sorted = normalize(expected_connections)
        user_sorted = normalize(user_connections)
    except (TypeError, ValueError):
        return False, _error_message(variant_data, 'Las conexiones enviadas no tienen un formato válido.')
    if expected_sorted == user_sorted:
        return True, ''
    return False, _error_message(variant_data, 'Las conexiones de red no son correctas.')
