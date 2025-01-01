from __future__ import absolute_import

from dotenv import load_dotenv

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.

load_dotenv()

# Default is local environment
environment = "local"

if environment == "production":
    from .production import *
else:
    from .local import *
