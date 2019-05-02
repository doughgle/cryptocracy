import os
import tempfile

import pytest
from flask import Flask, Response

from key_authority import ka_service
from key_authority.ka_service import create_app


@pytest.fixture
def http_test_client():
    Flask.response_class = JsonPatchedResponse
    app = create_app()
    db_fd, app.config['DATABASE'] = tempfile.mkstemp()
    app.config['TESTING'] = True
    client = app.test_client()

    with app.app_context():
        ka_service.db.init_db()

    yield client

    os.close(db_fd)
    os.unlink(app.config['DATABASE'])


class JsonPatchedResponse(Response):
    """
    Adapts `json` property to `json()` method so that the interface matches the
    `requests` library.
    Used to replace the response object in :attr:`~flask.Flask.response_class`.
    """
    def json(self):
        return self.get_json()