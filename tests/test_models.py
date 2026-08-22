"""Tests for Fyyur models."""

import pytest
from datetime import datetime
from app import app, db, Venue, Artist, Show


class TestVenueModel:
    """Test cases for the Venue model."""
    
    def test_venue_creation(self, client):
        """Test creating a new venue."""
        with app.app_context():
            venue = Venue(
                name='Test Venue',
                city='Test City',
                state='TS',
                address='123 Test St',
                phone='555-1234'
            )
            db.session.add(venue)
            db.session.commit()
            
            assert venue.id is not None
            assert venue.name == 'Test Venue'
            assert venue.city == 'Test City'
    
    def test_venue_retrieval(self, client):
        """Test retrieving a venue from database."""
        with app.app_context():
            venue = Venue(
                name='Retrieve Test Venue',
                city='Test City',
                state='TS'
            )
            db.session.add(venue)
            db.session.commit()
            
            retrieved = Venue.query.filter_by(name='Retrieve Test Venue').first()
            assert retrieved is not None
            assert retrieved.name == 'Retrieve Test Venue'


class TestArtistModel:
    """Test cases for the Artist model."""
    
    def test_artist_creation(self, client):
        """Test creating a new artist."""
        with app.app_context():
            artist = Artist(
                name='Test Artist',
                city='Test City',
                state='TS'
            )
            db.session.add(artist)
            db.session.commit()
            
            assert artist.id is not None
            assert artist.name == 'Test Artist'
    
    def test_artist_retrieval(self, client):
        """Test retrieving an artist from database."""
        with app.app_context():
            artist = Artist(
                name='Retrieve Test Artist',
                city='Test City',
                state='TS'
            )
            db.session.add(artist)
            db.session.commit()
            
            retrieved = Artist.query.filter_by(name='Retrieve Test Artist').first()
            assert retrieved is not None
            assert retrieved.name == 'Retrieve Test Artist'


class TestShowModel:
    """Test cases for the Show model."""

    def test_show_creation(self, client):
        """Test creating a new show."""
        with app.app_context():
            venue = Venue(name='Show Venue', city='City', state='ST')
            artist = Artist(name='Show Artist', city='City', state='ST')
            db.session.add_all([venue, artist])
            db.session.commit()

            show = Show(
                venue_id=venue.id,
                artist_id=artist.id,
                start_time=datetime(2024, 6, 1, 20, 0, 0)
            )
            db.session.add(show)
            db.session.commit()

            assert show.id is not None
            assert show.venue_id == venue.id
            assert show.artist_id == artist.id

    def test_show_relationships(self, client):
        """Test that Show has proper relationships to Venue and Artist."""
        with app.app_context():
            venue = Venue(name='Rel Venue', city='City', state='ST')
            artist = Artist(name='Rel Artist', city='City', state='ST')
            db.session.add_all([venue, artist])
            db.session.commit()

            show = Show(
                venue_id=venue.id,
                artist_id=artist.id,
                start_time=datetime(2024, 7, 4, 21, 0, 0)
            )
            db.session.add(show)
            db.session.commit()

            assert show in venue.shows
            assert show in artist.shows
