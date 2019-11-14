# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, you can obtain one at http://mozilla.org/MPL/2.0/.
import logging

import jwt
from redash.authentication import create_and_login_user, login_manager
from redash.authentication import request_loader as redash_request_loader
from redash.authentication.org_resolving import current_org
from redash.handlers.base import BaseResource
from redash.models import NoResultFound, User
from redash.permissions import require_permission
from werkzeug.exceptions import Unauthorized

from . import settings
from .resources import add_resource

logger = logging.getLogger(__name__)


def iodide_request_loader(request):
    user = None

    # TODO: parse JWT token using shared secret
    jwt_token = request.headers.get(settings.IODIDE_JWT_AUTH_HEADER, None)
    if jwt_token:
        org = current_org._get_current_object()

        try:
            # decode returns the claims which has the email if you need it
            payload = jwt.decode(
                jwt_token,
                key=settings.IODIDE_JWT_AUTH_KEY,
                issuer=settings.IODIDE_JWT_AUTH_ISSUER,
                audience=settings.IODIDE_JWT_AUTH_AUDIENCE,
                algorithms=settings.IODIDE_JWT_AUTH_ALGORITHMS,
            )
            if payload["sub"] != settings.IODIDE_JWT_AUTH_SUBJECT:
                raise Exception("Wrong subject: {}".format(payload["sub"]))
        except Exception as e:
            logging.exception(e)
            raise Unauthorized("Invalid JWT token")
        else:
            try:
                user = User.get_by_email_and_org(payload["email"], org)
            except NoResultFound:
                user = create_and_login_user(
                    current_org, payload["email"], payload["email"]
                )

    if user:
        return user
    else:
        return redash_request_loader(request)


class IodideQueryBackendResource(BaseResource):
    @require_permission("view_query")
    def post(self):
        pass


def extension(app):
    logger.info("Loading Iodide kernel extension")
    # Add a hook for our custom request loader
    login_manager.request_loader(iodide_request_loader)
    add_resource(
        app,
        IodideQueryBackendResource,
        "/api/integrations/iodide/query",
        endpoint="idodide_query",
    )
    logger.info("Loaded Iodide kernel extension")
