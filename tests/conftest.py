"""Pytest configuration and fixtures for Fyyur tests."""

import os
import pytest
import sqlalchemy as sa
from app import app, db

_TEST_DB_URI = 'sqlite:///:memory:'


@pytest.fixture
def client():
    """Create a test client with a test database."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = _TEST_DB_URI

    # Flask-SQLAlchemy 3.x caches engines in `_app_engines` keyed by app instance.
    # Updating `SQLALCHEMY_DATABASE_URI` alone does not recreate the cached engine.
    # Calling `init_app` again raises an error (already registered), and after the
    # first request Flask also blocks new `teardown_appcontext` registrations.
    # Directly replacing the cached engine is therefore the only way to swap the
    # database URI for test isolation without an app-factory pattern.
    if app in db._app_engines:
        for engine in db._app_engines[app].values():
            engine.dispose()
        db._app_engines[app].clear()
    else:
        db._app_engines.setdefault(app, {})
    db._app_engines[app][None] = sa.create_engine(_TEST_DB_URI)

    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.session.remove()
        db.drop_all()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()
