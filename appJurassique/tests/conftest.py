import pytest
from click.testing import CliRunner
from appJurassique import app, db, commands
from appJurassique.models import *
from hashlib import sha256


@pytest.fixture
def testapp():
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "WTF_CSRF_ENABLED": False,
        "LOGIN_DISABLED": False,
        "SECRET_KEY": "test-secret-key"
    })

    with app.app_context():
        db.create_all()
        db.session.commit()
    yield app

    # Cleanup après les tests
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(testapp):
    return testapp.test_client()


@pytest.fixture
def runner(testapp):
    return testapp.test_cli_runner()
