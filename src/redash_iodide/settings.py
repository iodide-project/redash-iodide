# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import logging
import os

from redash.handlers.base import BaseResource
from redash.permissions import require_permission

from .resources import add_resource

logger = logging.getLogger(__name__)


# The base URL of Mozilla's private Iodide instance
IODIDE_URL = os.environ.get("REDASH_IODIDE_URL", "")

# The Iodide API endpoint to hit to create a new notebook
IODIDE_NOTEBOOK_API_URL = os.environ.get("REDASH_IODIDE_NOTEBOOK_API_URL", "")

# The auth token that this extension uses to create new Iodide notebooks
IODIDE_AUTH_TOKEN = os.environ.get("REDASH_IODIDE_AUTH_TOKEN", "")


class IodideSettingsResource(BaseResource):
    @require_permission("view_query")
    def get(self):
        return {"iodideURL": IODIDE_URL}


def extension(app):
    logger.info("Loading Iodide setting extension")
    add_resource(
        app,
        IodideSettingsResource,
        "/api/integrations/iodide/settings",
        endpoint="idodide_settings",
    )
    logger.info("Loaded Iodide setting extension")
