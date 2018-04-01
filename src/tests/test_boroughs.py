from flask import url_for
from datetime import datetime
import pytest


def _get_boroughs(testapp, **kwargs):
    return testapp.get(url_for('api.get_boroughs'), **kwargs)


def _get_borough(testapp, id, **kwargs):
    return testapp.get(url_for('api.get_borough', id=id), **kwargs)


def _post_borough(testapp, name, **kwargs):
    return testapp.post_json(url_for('api.create_borough'), {
        "name": name
    }, **kwargs)


def _put_borough(testapp, name, id, **kwargs):
    return testapp.put_json(url_for('api.update_borough', id=id), {
        "name": name
    }, **kwargs)


def _patch_borough(testapp, name, id, **kwargs):
    return testapp.patch_json(url_for('api.partial_update_borough', id=id), {
        "name": name
    }, **kwargs)


def _delete_borough(testapp, id, **kwargs):
    return testapp.delete(url_for('api.delete_borough', id=id), **kwargs)


@pytest.mark.usefixtures('db')
class TestBoroughs:

    def test_response_headers(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _get_borough(testapp, 1)
        assert resp.headers['Content-Type'] == 'application/json'
        multi_resp = _get_boroughs(testapp)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_boroughs(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_borough(testapp, 'queens')
        resp = testapp.get(url_for('api.get_boroughs'))
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json['items'][0]['name'] == 'manhattan'
        assert resp.json['items'][1]['name'] == 'queens'

    def test_get_borough(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _get_borough(testapp, 1)
        assert resp.status_code == 200
        assert resp.json['id'] == 1

    def test_create_borough(self, testapp):
        resp = _post_borough(testapp, 'manhattan')
        assert resp.status_code == 201
        assert resp.json['id'] == 1
        assert resp.json['name'] == 'manhattan'

    def test_update_borough(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _put_borough(testapp, 'brooklyn', 1)
        assert resp.status_code == 204
        get_resp = _get_borough(testapp, 1)
        assert get_resp.json['name'] == 'brooklyn'

    def test_partial_update_borough(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _patch_borough(testapp, 'brooklyn', 1)
        assert resp.status_code == 204
        get_resp = _get_borough(testapp, 1)
        assert get_resp.json['name'] == 'brooklyn'

    def test_delete_boroughs(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _delete_borough(testapp, 1)
        assert resp.status_code == 204

    def test_empty_create_borough(self, testapp):
        resp = testapp.post_json(url_for('api.create_borough'), {
        }, expect_errors=True)
        assert resp.status_code == 400

    def test_empty_update_borough(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = testapp.put_json(url_for('api.update_borough', id=1), {
        }, expect_errors=True)
        assert resp.status_code == 400

    def test_empty_partial_update_borough(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = testapp.put_json(url_for('api.partial_update_borough', id=1), {
        }, expect_errors=True)
        assert resp.status_code == 400

    def test_404_borough(self, testapp):
        resp = _patch_borough(testapp, 'brooklyn', 2, expect_errors=True)
        assert resp.status_code == 404

    def test_rate_limiter(self, testapp):
        _post_borough(testapp, 'manhattan')
        _get_borough(testapp, 1, expect_errors=True)
        _get_borough(testapp, 1, expect_errors=True)
        resp = _get_borough(testapp, 1, expect_errors=True)
        assert resp.status_code == 429
