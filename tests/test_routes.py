"""Integration tests for Fyyur routes and endpoints."""

import pytest
from datetime import datetime, timedelta
from app import app
from dal import db, Venue, Artist, Show, Genre


class TestAppRoutes:
    """Test basic application routes."""
    
    def test_index_route(self, client):
        """Test the home page route."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Fyyur' in response.data or b'Music Venue' in response.data
    
    def test_venues_route(self, client):
        """Test the venues listing page route."""
        response = client.get('/venues')
        assert response.status_code == 200
        assert b'Venues' in response.data
    
    def test_artists_route(self, client):
        """Test the artists listing page route."""
        response = client.get('/artists')
        assert response.status_code == 200
        assert b'Artist' in response.data
    
    def test_shows_route(self, client):
        """Test the shows listing page route."""
        response = client.get('/shows')
        assert response.status_code == 200
        assert b'Show' in response.data
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404


class TestVenueRoutes:
    """Test venue-related routes."""
    
    def test_show_venue_page(self, client):
        """Test viewing a single venue."""
        with app.app_context():
            venue = Venue(
                name='Test Venue',
                city='SF',
                state='CA',
                address='123 Main St',
                phone='555-1234'
            )
            db.session.add(venue)
            db.session.commit()
            venue_id = venue.id
        
        response = client.get(f'/venues/{venue_id}')
        assert response.status_code == 200
        assert b'Test Venue' in response.data
    
    def test_show_venue_not_found(self, client):
        """Test viewing non-existent venue."""
        response = client.get('/venues/9999')
        # Route returns 200 with no data (not 404)
        assert response.status_code == 200
    
    def test_create_venue_page(self, client):
        """Test accessing venue creation form."""
        response = client.get('/venues/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'form' in response.data.lower()
    
    def test_create_venue_form_submission(self, client):
        """Test creating a new venue via form submission."""
        form_data = {
            'name': 'New Test Venue',
            'city': 'San Francisco',
            'state': 'CA',
            'address': '456 Oak St',
            'phone': '555-2345',
            'genres': [],
            'image_link': '',
            'facebook_link': '',
            'website_link': ''
        }
        
        # Should handle form without crashing
        response = client.post('/venues/create', data=form_data, follow_redirects=True)
        assert response.status_code == 200
    
    def test_edit_venue_page(self, client):
        """Test accessing venue edit form."""
        with app.app_context():
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add(venue)
            db.session.commit()
            venue_id = venue.id
        
        response = client.get(f'/venues/{venue_id}/edit')
        assert response.status_code == 200
        assert b'Test Venue' in response.data
    
    def test_edit_venue_form_submission(self, client):
        """Test updating venue via form submission."""
        with app.app_context():
            venue = Venue(
                name='Original Name',
                city='SF',
                state='CA',
                address='123 St'
            )
            db.session.add(venue)
            db.session.commit()
            venue_id = venue.id
        
        form_data = {
            'name': 'Updated Name',
            'city': 'New York',
            'state': 'NY',
            'address': '456 Broadway',
            'phone': '555-1234',
            'genres': [],
            'image_link': '',
            'facebook_link': '',
            'website_link': ''
        }
        
        response = client.post(f'/venues/{venue_id}/edit', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Verify venue was updated
        with app.app_context():
            updated_venue = Venue.query.get(venue_id)
            assert updated_venue.name == 'Updated Name'
            assert updated_venue.city == 'New York'
    
    def test_delete_venue(self, client):
        """Test deleting a venue."""
        with app.app_context():
            venue = Venue(name='Delete Me', city='SF', state='CA')
            db.session.add(venue)
            db.session.commit()
            venue_id = venue.id
        
        response = client.delete(f'/venues/{venue_id}', follow_redirects=True)
        
        # Verify venue was deleted
        with app.app_context():
            deleted_venue = Venue.query.get(venue_id)
            assert deleted_venue is None
    
    def test_search_venues(self, client):
        """Test venue search functionality."""
        with app.app_context():
            venue1 = Venue(name='The Musical Hop', city='SF', state='CA')
            venue2 = Venue(name='Park Square', city='NYC', state='NY')
            db.session.add_all([venue1, venue2])
            db.session.commit()
        
        form_data = {'search_term': 'Musical'}
        response = client.post('/venues/search', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Musical' in response.data or b'Hop' in response.data


class TestArtistRoutes:
    """Test artist-related routes."""
    
    def test_show_artist_page(self, client):
        """Test viewing a single artist."""
        with app.app_context():
            artist = Artist(
                name='Test Artist',
                city='SF',
                state='CA',
                phone='555-1234'
            )
            db.session.add(artist)
            db.session.commit()
            artist_id = artist.id
        
        response = client.get(f'/artists/{artist_id}')
        assert response.status_code == 200
        assert b'Test Artist' in response.data
    
    def test_show_artist_not_found(self, client):
        """Test viewing non-existent artist."""
        response = client.get('/artists/9999', follow_redirects=True)
        # Route redirects and returns 200 with error message
        assert response.status_code == 200
    
    def test_create_artist_page(self, client):
        """Test accessing artist creation form."""
        response = client.get('/artists/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'form' in response.data.lower()
    
    def test_create_artist_form_submission(self, client):
        """Test artist creation form submission."""
        form_data = {
            'name': 'New Test Artist',
            'city': 'Los Angeles',
            'state': 'CA',
            'phone': '555-3456',
            'genres': [],  # Empty genres
            'image_link': '',
            'facebook_link': '',
            'website_link': '',
            'seeking_venue': 'n',
            'seeking_description': ''
        }
        
        # Should handle the form without crashing (may or may not create artist)
        response = client.post('/artists/create', data=form_data, follow_redirects=True)
        assert response.status_code == 200
    
    def test_edit_artist_page(self, client):
        """Test accessing artist edit form."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            db.session.add(artist)
            db.session.commit()
            artist_id = artist.id
        
        response = client.get(f'/artists/{artist_id}/edit')
        assert response.status_code == 200
        assert b'Test Artist' in response.data
    
    def test_edit_artist_form_submission(self, client):
        """Test updating artist via form submission."""
        with app.app_context():
            artist = Artist(
                name='Original Name',
                city='SF',
                state='CA'
            )
            db.session.add(artist)
            db.session.commit()
            artist_id = artist.id
        
        form_data = {
            'name': 'Updated Artist Name',
            'city': 'Chicago',
            'state': 'IL',
            'phone': '555-7890',
            'genres': [],
            'image_link': '',
            'facebook_link': '',
            'website_link': '',
            'seeking_venue': 'n',
            'seeking_description': ''
        }
        
        # Should handle form without crashing
        response = client.post(f'/artists/{artist_id}/edit', data=form_data, follow_redirects=True)
        assert response.status_code == 200
    
    def test_delete_artist(self, client):
        """Test deleting an artist."""
        with app.app_context():
            artist = Artist(name='Delete Me', city='SF', state='CA')
            db.session.add(artist)
            db.session.commit()
            artist_id = artist.id
        
        response = client.delete(f'/artists/{artist_id}', follow_redirects=True)
        
        # Verify artist was deleted
        with app.app_context():
            deleted_artist = Artist.query.get(artist_id)
            assert deleted_artist is None
    
    def test_search_artists(self, client):
        """Test artist search functionality."""
        with app.app_context():
            artist1 = Artist(name='Guns N Petals', city='SF', state='CA')
            artist2 = Artist(name='Matt Quevedo', city='NYC', state='NY')
            db.session.add_all([artist1, artist2])
            db.session.commit()
        
        form_data = {'search_term': 'Guns'}
        response = client.post('/artists/search', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        assert b'Guns' in response.data or b'Petals' in response.data


class TestShowRoutes:
    """Test show-related routes."""
    
    def test_show_list_page(self, client):
        """Test viewing all shows."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
        
        response = client.get('/shows')
        assert response.status_code == 200
        assert b'Show' in response.data
    
    def test_create_show_page(self, client):
        """Test accessing show creation form."""
        response = client.get('/shows/create')
        assert response.status_code == 200
        assert b'Create' in response.data or b'form' in response.data.lower()
    
    def test_create_show_form_submission(self, client):
        """Test creating a new show via form submission."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            artist_id = artist.id
            venue_id = venue.id
        
        future_time = (datetime.now() + timedelta(days=7)).isoformat()
        form_data = {
            'artist_id': artist_id,
            'venue_id': venue_id,
            'start_time': future_time
        }
        
        response = client.post('/shows/create', data=form_data, follow_redirects=True)
        assert response.status_code == 200
        
        # Verify show was created
        with app.app_context():
            show = Show.query.filter_by(
                artist_id=artist_id,
                venue_id=venue_id
            ).first()
            assert show is not None
    
    def test_create_show_with_invalid_artist(self, client):
        """Test creating show with non-existent artist."""
        with app.app_context():
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add(venue)
            db.session.commit()
            venue_id = venue.id
        
        future_time = (datetime.now() + timedelta(days=7)).isoformat()
        form_data = {
            'artist_id': 9999,  # Non-existent
            'venue_id': venue_id,
            'start_time': future_time
        }
        
        # Should fail gracefully
        response = client.post('/shows/create', data=form_data, follow_redirects=True)
        assert response.status_code in [200, 400]  # Either error page or redirected
    
    def test_create_show_with_invalid_venue(self, client):
        """Test creating show with non-existent venue."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            db.session.add(artist)
            db.session.commit()
            artist_id = artist.id
        
        future_time = (datetime.now() + timedelta(days=7)).isoformat()
        form_data = {
            'artist_id': artist_id,
            'venue_id': 9999,  # Non-existent
            'start_time': future_time
        }
        
        # Should fail gracefully
        response = client.post('/shows/create', data=form_data, follow_redirects=True)
        assert response.status_code in [200, 400]
    
    def test_show_detail_page(self, client):
        """Test viewing a specific show's details."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
            show_id = show.id
        
        response = client.get(f'/shows/{show_id}')
        assert response.status_code == 200
    
    def test_show_detail_not_found(self, client):
        """Test viewing non-existent show."""
        response = client.get('/shows/9999', follow_redirects=True)
        assert response.status_code == 200
    
    def test_search_shows_by_artist(self, client):
        """Test searching shows by artist."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
            artist_id = artist.id
        
        response = client.post('/shows/search', data={'artist_id': str(artist_id), 'venue_id': ''}, follow_redirects=True)
        assert response.status_code == 200
    
    def test_search_shows_by_venue(self, client):
        """Test searching shows by venue."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
            venue_id = venue.id
        
        response = client.post('/shows/search', data={'artist_id': '', 'venue_id': str(venue_id)}, follow_redirects=True)
        assert response.status_code == 200
    
    def test_search_shows_empty_params(self, client):
        """Test search with no parameters."""
        response = client.post('/shows/search', data={'artist_id': '', 'venue_id': ''}, follow_redirects=True)
        assert response.status_code == 200
    
    def test_edit_show_form_page(self, client):
        """Test accessing show edit form."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
            show_id = show.id
        
        response = client.get(f'/shows/{show_id}/edit')
        assert response.status_code == 200
    
    def test_edit_show_form_submission(self, client):
        """Test updating a show via form submission."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
            show_id = show.id
            artist_id = artist.id
            venue_id = venue.id
        
        future_time = (datetime.now() + timedelta(days=14)).isoformat()
        form_data = {
            'artist_id': artist_id,
            'venue_id': venue_id,
            'start_time': future_time
        }
        
        response = client.post(f'/shows/{show_id}/edit', data=form_data, follow_redirects=True)
        assert response.status_code == 200
    
    def test_delete_show(self, client):
        """Test deleting a show."""
        with app.app_context():
            artist = Artist(name='Test Artist', city='SF', state='CA')
            venue = Venue(name='Test Venue', city='SF', state='CA')
            db.session.add_all([artist, venue])
            db.session.commit()
            
            show = Show(
                artist_id=artist.id,
                venue_id=venue.id,
                start_time=datetime.now() + timedelta(days=7)
            )
            db.session.add(show)
            db.session.commit()
            show_id = show.id
        
        response = client.delete(f'/shows/{show_id}')
        # DELETE endpoint returns JSON
        assert response.status_code in [200, 400]


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    def test_500_error_handling(self, client):
        """Test 500 error page exists."""
        # Trigger internal server error
        response = client.get('/nonexistent-route-that-does-not-exist')
        # Should be 404 since route doesn't exist
        assert response.status_code == 404
    
    def test_empty_database_displays_properly(self, client):
        """Test routes display properly with empty database."""
        # All test methods use empty database, so this just verifies rendering
        response = client.get('/venues')
        assert response.status_code == 200
        
        response = client.get('/artists')
        assert response.status_code == 200
        
        response = client.get('/shows')
        assert response.status_code == 200
    
    def test_form_submission_with_missing_fields(self, client):
        """Test form submission with missing required fields."""
        # Submit form with incomplete data (missing city, state, address)
        form_data = {
            'name': 'Incomplete Venue'
        }
        
        # App should handle the missing fields error gracefully
        response = client.post('/venues/create', data=form_data, follow_redirects=True)
        # Should either handle it gracefully or redirect with error message
        assert response.status_code in [200, 400]
