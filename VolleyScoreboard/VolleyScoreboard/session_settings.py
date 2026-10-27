"""Configuração usada pela aplicação para manter a partida fora do banco."""

from .settings import *  # noqa: F403

# O estado é assinado, mas não criptografado: guarde apenas dados pequenos e não sensíveis.
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
