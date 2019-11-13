# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import logging
import os

from redash.handlers.base import BaseResource
from redash.permissions import require_permission
from redash.settings.helpers import array_from_string

from .resources import add_resource

logger = logging.getLogger(__name__)


# The base URL of Mozilla's private Iodide instance
IODIDE_URL = os.environ.get("REDASH_IODIDE_URL", "")

# The Iodide API endpoint to hit to create a new notebook
IODIDE_NOTEBOOK_API_URL = os.environ.get("REDASH_IODIDE_NOTEBOOK_API_URL", "")

# The auth token that this extension uses to create new Iodide notebooks
IODIDE_AUTH_TOKEN = os.environ.get("REDASH_IODIDE_AUTH_TOKEN", "")

# The JWT request header for authenticating Iodide requests
IODIDE_JWT_AUTH_HEADER = os.environ.get("REDASH_IODIDE_JWT_AUTH_HEADER", "")

# The shared secret key
IODIDE_JWT_AUTH_KEY = os.environ.get("REDASH_IODIDE_JWT_AUTH_KEY", "")

IODIDE_JWT_AUTH_ISSUER = os.environ.get(
    "REDASH_IODIDE_JWT_AUTH_ISSUER", "https://iodide.io/"
)

IODIDE_JWT_AUTH_AUDIENCE = os.environ.get("REDASH_IODIDE_JWT_AUTH_AUDIENCE", "")

IODIDE_JWT_AUTH_SUBJECT = os.environ.get(
    "REDASH_IODIDE_JWT_AUTH_SUBJECT", "query:create"
)

IODIDE_JWT_AUTH_ALGORITHMS = array_from_string(
    os.environ.get("REDASH_IODIDE_JWT_AUTH_ALGORITHMS", "ES256")
)


class IodideSettingsResource(BaseResource):
    @require_permission("view_query")
    def get(self):
        return {"iodideURL": IODIDE_URL}


def extension(app):
    logger.info("Loading Iodide setting extension")
    add_resource(app, IodideSettingsResource, "/api/integrations/iodide/settings")
    logger.info("Loaded Iodide setting extension")
