"""
WSGI config for VolleyScoreboard project.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "VolleyScoreboard.session_settings")

application = get_wsgi_application()
