# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
from redash.handlers.api import api


def add_resource(app, *args, **kwargs):
    """
    After api.init_app() is called, api.app should be set by Flask (but it's not) so that
    further calls to add_resource() are handled immediately for the given app.
    """
    api.app = app
    api.add_org_resource(*args, **kwargs)
