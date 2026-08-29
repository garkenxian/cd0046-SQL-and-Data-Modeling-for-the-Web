"""Pytest configuration and fixtures for Fyyur tests."""

import os
import pytest
from datetime import datetime

# CRITICAL: Set test database BEFORE importing app to ensure it uses SQLite
os.environ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

from app import app
from dal import db
from dto.venue import VenueDTO
from dto.artist import ArtistDTO
from dto.show import ShowDTO


@pytest.fixture(scope='function', autouse=True)
def _ensure_test_database():
    """Ensure we NEVER connect to production database during tests.
    
    This runs before every test to verify the database is SQLite.
    """
    current_uri = app.config.get('SQLALCHEMY_DATABASE_URI', '')
    
    # Safety check: NEVER allow PostgreSQL connections during tests
    if 'postgresql' in current_uri.lower() or 'postgres' in current_uri.lower():
        raise RuntimeError(
            f"CRITICAL: Test attempted to use production database! "
            f"Database URI: {current_uri}\n"
            f"Tests must ONLY use SQLite (sqlite:///:memory:). "
            f"Set SQLALCHEMY_DATABASE_URI environment variable before running tests."
        )
    
    # Ensure we're using SQLite
    if 'sqlite' not in current_uri.lower():
        raise RuntimeError(
            f"CRITICAL: Test database is not SQLite! "
            f"Current URI: {current_uri}\n"
            f"Tests must use SQLite only. Set SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'"
        )


@pytest.fixture
def client():
    """Create a test client with an in-memory SQLite database."""
    # Ensure test mode is enabled
    app.config['TESTING'] = True
    
    with app.app_context():
        # Dispose of any stale connections
        db.engine.dispose()
        
        # Create all tables for this test
        db.create_all()
        
        yield app.test_client()
        
        # Cleanup after test
        db.session.remove()
        db.drop_all()
        db.engine.dispose()


@pytest.fixture
def runner(app):
    """Create a test CLI runner."""
    return app.test_cli_runner()


# ============================================================================
# Helper Functions for Creating DTOs
# ============================================================================

def create_venue_dto(name='Test Venue', city='SF', state='CA', address='123 St', phone='555-1234', genres=None):
    """Helper to create VenueDTO objects."""
    if genres is None:
        genres = []
    return VenueDTO(
        id=None,
        name=name,
        city=city,
        state=state,
        address=address,
        phone=phone,
        image_link='http://image.com/test.jpg',
        facebook_link='http://facebook.com/test',
        website='http://test.com',
        genres=genres
    )


def create_artist_dto(name='Test Artist', city='SF', state='CA', phone='555-1234', genres=None):
    """Helper to create ArtistDTO objects."""
    if genres is None:
        genres = []
    return ArtistDTO(
        id=None,
        name=name,
        city=city,
        state=state,
        phone=phone,
        image_link='http://image.com/test.jpg',
        facebook_link='http://facebook.com/test',
        website='http://test.com',
        genres=genres,
        seeking_venue=False,
        seeking_description=''
    )


def create_show_dto(artist_id, venue_id, start_time):
    """Helper to create ShowDTO objects."""
    return ShowDTO(
        id=None,
        artist_id=artist_id,
        venue_id=venue_id,
        start_time=start_time.isoformat() if isinstance(start_time, datetime) else start_time
    )
