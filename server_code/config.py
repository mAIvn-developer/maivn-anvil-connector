"""API key resolution. Anvil-runtime-safe (no annotations)."""

import anvil.secrets

_SECRET_NAME = "MAIVN_API_KEY"


class MaivnConfigError(RuntimeError):
    """Raised when required connector configuration is missing."""


def resolve_api_key(explicit=None):
    """Return the mAIvn API key, preferring an explicit value over the secret."""
    if explicit:
        return explicit
    try:
        return anvil.secrets.get_secret(_SECRET_NAME)
    except Exception as exc:  # noqa: BLE001 - any secret-store failure is a config error
        raise MaivnConfigError(
            f"Set the '{_SECRET_NAME}' App Secret (Anvil -> Secrets) or pass api_key explicitly."
        ) from exc
