import json
import os

import mock
from mock import patch
from redash_iodide import settings
from six.moves import reload_module
from tests import BaseTestCase, authenticate_request


class TestIodideIntegration(BaseTestCase):
    SETTING_OVERRIDES = {"REDASH_IODIDE_URL": "https://example.com/"}

    def setUp(self):
        super(TestIodideIntegration, self).setUp()
        self.admin = self.factory.create_admin()

        self.data_source_default = self.factory.create_data_source(
            group=self.factory.default_group
        )
        variables = self.SETTING_OVERRIDES.copy()
        with patch.dict(os.environ, variables):
            reload_module(settings)

        # Queue a cleanup routine that reloads the settings without overrides
        # once the test ends
        self.addCleanup(lambda: reload_module(settings))
        authenticate_request(self.client, self.admin)

    def test_settings(self):
        rv = self.client.get("/api/integrations/iodide/settings",)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(
            rv.data,
            json.dumps({"iodideURL": self.SETTING_OVERRIDES["REDASH_IODIDE_URL"]}),
        )

    @mock.patch("requests.post")
    def test_notebook_post_allowed(self, mock_post):
        data_source = self.factory.create_data_source(
            group=self.factory.default_group
        )

        query = self.factory.create_query(
            user=self.admin,
            data_source=data_source,
            query_text="select * from events",
        )

        # Iodide should return a notebook ID. The notebook ID that it returns
        # is unrelated to the query ID that we pass it.
        iodide_notebook_id = 99

        mock_value = {"id": iodide_notebook_id}
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.text = json.dumps(mock_value)
        mock_json = mock.Mock()
        mock_json.return_value = mock_value
        mock_response.json = mock_json
        mock_post.return_value = mock_response

        rv = self.client.post("/api/integrations/iodide/%s/notebook" % query.id)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.data, json.dumps({"id": iodide_notebook_id}))

    @mock.patch("requests.post")
    def test_notebook_post_disallowed(self, mock_post):
        data_source = self.factory.create_data_source(
            group=self.factory.admin_group
        )

        query = self.factory.create_query(
            user=self.admin,
            data_source=data_source,
            query_text="select * from events",
        )

        rv = self.client.post("/api/integrations/iodide/%s/notebook" % query.id)
        self.assertEquals(rv.status_code, 200)
        self.assertEquals(rv.data, json.dumps({"message": "Couldn't find resource. Please login and try again."}))
