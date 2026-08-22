"""Tests for Fyyur routes and endpoints."""

import pytest
from app import app


class TestAppRoutes:
    """Test cases for application routes."""
    
    def test_index_route(self, client):
        """Test the home page route."""
        response = client.get('/')
        assert response.status_code == 200
    
    def test_venues_route(self, client):
        """Test the venues listing page route."""
        response = client.get('/venues')
        assert response.status_code == 200
    
    def test_artists_route(self, client):
        """Test the artists listing page route."""
        response = client.get('/artists')
        assert response.status_code == 200
    
    def test_shows_route(self, client):
        """Test the shows listing page route."""
        response = client.get('/shows')
        assert response.status_code == 200
    
    def test_404_error(self, client):
        """Test 404 error handling."""
        response = client.get('/nonexistent')
        assert response.status_code == 404
