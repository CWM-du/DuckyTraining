from rest_framework import serializers

# 1. OUTBOUND: Lo que le enviamos a React (El ejercicio limpio)
class FindErrorVariantSerializer(serializers.Serializer):
    """
    Serializa la variante desde la memoria hacia el frontend.
    Omite deliberadamente 'expected_bug_id' y 'explanation' por seguridad.
    """
    id = serializers.CharField()
    nivel = serializers.IntegerField()
    # Enviamos la lista de líneas: [{"id": 0, "linea": "x == 10"}, {"id": 1, ...}]
    codigo = serializers.ListField(
        child=serializers.DictField()
    )


# 2. INBOUND: Lo que recibimos de React (La respuesta del usuario)
class AnswerSubmissionSerializer(serializers.Serializer):
    """
    Valida el payload (answer_payload) enviado por el frontend 
    antes de registrar el intento y calcular recompensas.
    """
    # Para el juego 'Encuentra el fallo'
    selected_bug_id = serializers.CharField(required=False)
    
    # Para los otros juegos (puedes unificar el endpoint recibiendo campos opcionales)
    ordered_ids = serializers.ListField(
        child=serializers.CharField(), required=False
    )
    connections = serializers.ListField(
        child=serializers.ListField(child=serializers.CharField()), required=False
    )