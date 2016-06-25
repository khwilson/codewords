import requests

from codewords import __version__


def test_index_route(server):
    host, port = server
    response = requests.get('http://{host}:{port}/'.format(host=host, port=port))
    assert response.ok
    assert b'Welcome!' in response.content


def test_version():
    """
    Assert that the version is what we expect it to be.
    You should delete this test before you actually start doing things.
    """
    assert __version__ == '0.1.dev0'
