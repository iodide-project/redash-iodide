# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import logging

from redash.handlers.base import BaseResource, get_object_or_404
from redash.models import Query
from redash.permissions import require_permission

from .resources import add_resource

logger = logging.getLogger(__name__)


class IodideGroupsResource(BaseResource):
    @require_permission("view_query")
    def get(self, query_id):
        groups = get_object_or_404(Query.all_groups_for_query_ids, query_id)
        group_ids = [g[0] for g in groups]
        return {"groups": group_ids}


def extension(app):
    logger.info("Loading Iodide groups extension")
    add_resource(
        app,
        IodideGroupsResource,
        "/api/integrations/iodide/<query_id>/groups",
        endpoint="iodide_groups",
    )
    logger.info("Loaded Iodide groups extension")
