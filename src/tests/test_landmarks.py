from flask import url_for
from datetime import datetime, date
import pytest


def _post_borough(testapp, name, **kwargs):
    return testapp.post_json(url_for('api.create_borough'), {
        "name": name
    }, **kwargs)


def _get_landmarks(testapp, boroughId, **kwargs):
    return testapp.get(
        "/api/boroughs/{0}/landmarks".format(boroughId), **kwargs)


def _get_landmark(testapp, boroughId, id, **kwargs):
    return testapp.get(
        "/api/boroughs/{0}/landmarks/{1}".format(boroughId, id), **kwargs)


def _post_landmark(testapp, boroughId, name, description, **kwargs):
    return testapp.post_json(
        "/api/boroughs/{0}/landmarks".format(boroughId), {
            "name": name,
            "description": description
        }, **kwargs)


def _put_landmark(testapp, boroughId, id, name, description, **kwargs):
    return testapp.put_json(
        "/api/boroughs/{0}/landmarks/{1}".format(boroughId, id), {
            "name": name,
            "description": description
        }, **kwargs)


def _patch_landmark(testapp, boroughId, id, name, **kwargs):
    return testapp.patch_json(
        "/api/boroughs/{0}/landmarks/{1}".format(boroughId, id), {
            "name": name
        }, **kwargs)


def _delete_landmark(testapp, boroughId, id, **kwargs):
    return testapp.delete(
        "/api/boroughs/{0}/landmarks/{1}".format(boroughId, id), **kwargs)


@pytest.mark.usefixtures('db')
class TestLandmarks:

    def test_response_headers(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = _get_landmark(testapp, 1, 1)
        assert resp.headers['Content-Type'] == 'application/json'

    def test_get_landmarks(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        _post_landmark(testapp, 1, '1 wall street', 'art deco style')
        resp = _get_landmarks(testapp, 1)
        assert resp.status_code == 200
        assert resp.headers['Content-Type'] == 'application/json'
        assert resp.json['items'][0]['name'] == 'woolworth'
        assert resp.json['items'][1]['name'] == '1 wall street'

    def test_get_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = _get_landmark(testapp, 1, 1)
        assert resp.status_code == 200
        assert resp.json['items'][0]['id'] == 1

    def test_create_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _post_landmark(testapp, 1, 'woolworth', 'tall building')
        assert resp.status_code == 201
        assert resp.json['id'] == 1

    def test_update_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = _put_landmark(testapp, 1, 1, 'woolworth', 'old building')
        assert resp.status_code == 204
        get_resp = _get_landmark(testapp, 1, 1)
        assert get_resp.json['items'][0]['description'] == 'old building'

    def test_partial_update_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = _patch_landmark(testapp, 1, 1, 'empire')
        assert resp.status_code == 204
        get_resp = _get_landmark(testapp, 1, 1)
        assert get_resp.json['items'][0]['name'] == 'empire'
        assert get_resp.json['items'][0]['description'] == 'tall building'

    def test_delete_landmarks(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = _delete_landmark(testapp, 1, 1)
        assert resp.status_code == 204

    def test_empty_create_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = testapp.post_json(
            "/api/boroughs/{0}/landmarks".format(1), {
            }, expect_errors=True)
        assert resp.status_code == 400

    def test_empty_update_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = testapp.put_json(
            "/api/boroughs/{0}/landmarks/{1}".format(1, 1), {
            }, expect_errors=True)
        assert resp.status_code == 400

    def test_empty_partial_update_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        _post_landmark(testapp, 1, 'woolworth', 'tall building')
        resp = testapp.patch_json(
            "/api/boroughs/{0}/landmarks/{1}".format(1, 1), {
            }, expect_errors=True)
        assert resp.status_code == 204

    def test_404_landmark(self, testapp):
        _post_borough(testapp, 'manhattan')
        resp = _patch_landmark(testapp, 1, 1, 'empire', expect_errors=True)
        assert resp.status_code == 404
