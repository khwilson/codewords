from __future__ import print_function, unicode_literals

import os
import random
import shutil
import subprocess
import tempfile
import time

import pytest

from codewords.app import app, db as the_db


@pytest.fixture(scope='session')
def database(request):
    tmpdir = tempfile.mkdtemp()
    db_path = os.path.join(tmpdir, 'test.db')
    print("Creating a database at {}".format(db_path))
    db_uri = 'sqlite:///' + db_path
    subprocess.check_call(['crun', 'create', db_uri])

    def fin():
        shutil.rmtree(tmpdir)
    request.addfinalizer(fin)

    return db_uri


@pytest.fixture(scope='session')
def server(request, database):
    """ Launch the server across the whole session """
    host = 'localhost'
    port = random.randint(50000, 60000)
    print("Starting a new server at {host}:{port}...".format(host=host, port=port))
    proc = subprocess.Popen(['crun', 'serve', '--host', host,
                             '--port', str(port), '--debug', database])

    request.addfinalizer(proc.kill)

    # Sleep to guarantee server is up
    time.sleep(2)

    return host, port


@pytest.fixture(scope='session')
def db(database):
    app.config['SQLALCHEMY_DATABASE_URI'] = database
    return the_db
