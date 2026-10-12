def validate_sorting(variant_data, user_answer):
    """
    Valida el formato 'Ordena el algoritmo'.
    Compara el orden enviado por el usuario con el expected_order de la variante.
    """
    expected_order = variant_data.get('expected_order', [])
    user_order = user_answer.get('ordered_ids', [])
    
    # Comprobación estricta de listas (mismos elementos en el mismo orden)
    if expected_order == user_order:
        return True, ""
    
    # Si falla, devolvemos False y la explicación configurada en la variante
    explanation = variant_data.get('explanation', "El orden de los pasos no es correcto.")
    return False, explanation

def validate_bug_finding(variant_data, user_answer):
    """
    Valida el formato 'Encuentra el fallo'.
    Compara el ID seleccionado por el usuario con el esperado.
    """
    expected_bug_id = variant_data.get('expected_bug_id')
    user_bug_id = user_answer.get('selected_bug_id')
    
    if expected_bug_id and expected_bug_id == user_bug_id:
        return True, ""
        
    explanation = variant_data.get('explanation', "Ese no es el error principal.")
    return False, explanation

def validate_networking(variant_data, user_answer):
    """
    Valida el formato 'Conecta la red'.
    Compara las conexiones trazadas sin importar la dirección (A->B es igual a B->A)
    ni el orden en el que se trazaron.
    """
    expected_connections = variant_data.get('expected_connections', [])
    user_connections = user_answer.get('connections', [])
    
    try:
        # Ordenamos los elementos dentro de cada conexión (para que [B, A] pase a ser [A, B])
        # y luego ordenamos la lista general de conexiones.
        expected_sorted = sorted([sorted(conn) for conn in expected_connections])
        user_sorted = sorted([sorted(conn) for conn in user_connections])
        
        if expected_sorted == user_sorted:
            return True, ""
    except (TypeError, ValueError):
        # Si el frontend envía datos malformados (ej. no es una lista de listas)
        pass
        
    explanation = variant_data.get('explanation', "Las conexiones de red no son correctas.")
    return False, explanation