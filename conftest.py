from __future__ import print_function

import random
import subprocess
import time

import pytest


@pytest.fixture(scope='session')
def server(request):
    """ Launch the server across the whole session """
    host = 'localhost'
    port = random.randint(50000, 60000)
    print("Starting a new server at {host}:{port}...".format(host=host, port=port))
    proc = subprocess.Popen(['crun', 'serve', '--host', host,
                             '--port', str(port), '--debug'])

    request.addfinalizer(proc.kill)

    # Sleep to guarantee server is up
    time.sleep(2)

    return host, port
