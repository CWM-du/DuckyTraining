"""Carga y valida configuración provisional de integraciones; no contiene secretos."""
import json
from functools import lru_cache
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent / 'config.json'


class IntegrationConfigurationError(ValueError):
    """La configuración de integración no cumple el esquema esperado."""


@lru_cache(maxsize=1)
def load_integration_config():
    try:
        with CONFIG_PATH.open('r', encoding='utf-8') as stream:
            config = json.load(stream)
    except (OSError, json.JSONDecodeError) as exc:
        raise IntegrationConfigurationError('Configuración de integraciones no disponible o JSON inválido.') from exc

    if not isinstance(config, dict) or config.get('schema_version') != 1:
        raise IntegrationConfigurationError('Versión o estructura raíz de integración no válida.')
    if config.get('mode') != 'provisional' or config.get('timezone') != 'Europe/Madrid':
        raise IntegrationConfigurationError('Modo o zona horaria de integración no válida.')
    access_levels = config.get('access_levels')
    expected_levels = {'FREE', 'PLUS', 'PRO', 'ALUMNO_PLUS_TEMPORAL'}
    if (not isinstance(access_levels, dict) or set(access_levels) != expected_levels
            or not all(isinstance(value, dict) for value in access_levels.values())):
        raise IntegrationConfigurationError('La configuración de niveles de acceso está incompleta.')
    if access_levels['FREE'].get('daily_games') != 3:
        raise IntegrationConfigurationError('La regla diaria de Free debe ser de tres juegos.')
    if any(access_levels[level].get('daily_games') != 10 for level in ('PLUS', 'PRO', 'ALUMNO_PLUS_TEMPORAL')):
        raise IntegrationConfigurationError('Los niveles Plus deben permitir diez juegos diarios.')
    if access_levels['ALUMNO_PLUS_TEMPORAL'].get('requires_verified_future_expiry') is not True:
        raise IntegrationConfigurationError('El acceso temporal debe exigir caducidad futura verificable.')
    rewards = config.get('rewards')
    if not isinstance(rewards, dict):
        raise IntegrationConfigurationError('Falta la configuración de Rewards.')
    if rewards.get('xp_per_correct_attempt') != 5 or rewards.get('grant_enabled') is not False:
        raise IntegrationConfigurationError('La configuración no puede habilitar concesiones reales.')
    if rewards.get('coin_candidate_on_first_daily_completion') is not True:
        raise IntegrationConfigurationError('Regla de moneda no válida.')
    for key in ('provider_id',):
        if not isinstance(rewards.get(key), str) or not rewards[key].strip():
            raise IntegrationConfigurationError('Identificador de proveedor Rewards no válido.')
    membership = config.get('membership')
    if (not isinstance(membership, dict)
            or membership.get('provider_id') != 'team0_identity_membership_pending_contract'
            or membership.get('mode') != 'local_provisional_profile'):
        raise IntegrationConfigurationError('El adaptador de membresía oficial no está correctamente identificado.')
    bank = config.get('ducky_bank')
    if (not isinstance(bank, dict) or bank.get('grant_enabled') is not False
            or not isinstance(bank.get('provider_id'), str) or not bank['provider_id'].strip()):
        raise IntegrationConfigurationError('Duki Bank debe permanecer deshabilitado en modo provisional.')
    return config


def clear_integration_config_cache():
    load_integration_config.cache_clear()
