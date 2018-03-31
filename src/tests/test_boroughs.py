from flask import url_for
from datetime import datetime
import pytest


@pytest.mark.usefixtures('db')
class TestBoroughs:

    def test_create_borough(self, testapp):
        resp = testapp.post_json(url_for('api.create_borough'), {
            "name": 'friendbar'
        })
        assert resp.json['id'] == 1
        assert resp.status_code == 201

    def test_retreive_borough(self, testapp):
        testapp.post_json(url_for('api.create_borough'), {
            "name": 'friendbar'
        })
        resp = testapp.get(url_for('api.get_boroughs'))
        assert resp.status_code == 200
        assert resp.json['items'][0]['name'] == 'friendbar'
