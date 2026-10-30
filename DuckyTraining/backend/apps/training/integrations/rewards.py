"""Preparación de intenciones deterministas; nunca concede XP ni monedas reales."""
from .config import IntegrationConfigurationError, load_integration_config


def prepare_reward_intents(*, user_id, cycle_date, exercise_number, attempt_number,
                           is_correct, first_completion, xp_amount):
    """Prepara claves deduplicables para futuras integraciones; no las persiste ni procesa."""
    try:
        config = load_integration_config()
    except IntegrationConfigurationError:
        return {'status': 'disabled_invalid_config', 'events': []}

    if config['mode'] != 'provisional' or config['rewards']['grant_enabled'] is not False:
        return {'status': 'disabled_unsafe_configuration', 'events': []}
    if not is_correct:
        return {'status': 'no_reward_candidate', 'events': []}

    day = cycle_date.isoformat()
    events = [{
        'provider_id': config['rewards']['provider_id'],
        'event_key': f'training:xp:{user_id}:{day}:exercise:{exercise_number}:attempt:{attempt_number}',
        'kind': 'xp_candidate',
        'amount': int(xp_amount),
        'status': 'pending_contract',
        'granted': False,
    }]
    if first_completion and config['rewards']['coin_candidate_on_first_daily_completion']:
        events.append({
            'provider_id': config['ducky_bank']['provider_id'],
            'event_key': f'training:coin:{user_id}:{day}:exercise:{exercise_number}',
            'kind': 'ducky_coin_candidate',
            'amount': 1,
            'status': 'pending_contract',
            'granted': False,
        })
    return {'status': 'pending_contract', 'events': events}
