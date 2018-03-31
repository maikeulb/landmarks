from flask import url_for
from datetime import datetime
import pytest


def _register_borough(testapp, **kwargs):
    return testapp.post_json(url_for('api.create_borough'), {
        "name": 'friendbar'
    })


@pytest.mark.usefixtures('db')
class TestBoroughs:

    def test_create_borough(self, testapp):
        _register_borough(testapp)
        resp = testapp.get(url_for('api.get_boroughs'))
        assert resp.status_code == 200
        assert resp.json['items'][0]['name'] == 'friendbar'
