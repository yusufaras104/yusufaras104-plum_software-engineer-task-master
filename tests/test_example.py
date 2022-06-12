import pytest
from shorty.app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    # other setup can go here

    yield app

    # clean up / reset resources here
@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

@pytest.fixture()
def client(app):
    return app.test_client()


def test_bitly_OK(client):
    resp = client.post('/shortlinks', json={'url': 'http://asd.thing.com', 'provider': 'bit.ly'})
    print(resp)
    assert resp.status_code == 200
    assert resp.json.get('provider') == 'bitly'
    assert resp.json.get('url').startswith('https://bit.ly')
    print(resp.json.get('url'))

def test_tinyurl_OK(client):
    resp = client.post('/shortlinks', json={'url': 'http://asd.thing.com', 'provider': 'tinyurl.com'})
    print(resp)
    assert resp.status_code == 200
    assert resp.json.get('provider') == 'tinyurl'
    assert resp.json.get('url').startswith('https://tinyurl.com')
    print(resp.json.get('url'))