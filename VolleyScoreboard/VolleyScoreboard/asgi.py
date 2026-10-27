"""
ASGI config for VolleyScoreboard project.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VolleyScoreboard.session_settings")

application = get_asgi_application()
