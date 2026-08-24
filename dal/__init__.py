"""Data Access Layer - manages all database models and queries."""

from flask_sqlalchemy import SQLAlchemy

# Single shared database instance used across entire app
db = SQLAlchemy()

# Import models so they're registered with db
from dal.venue import Venue
from dal.artist import Artist

__all__ = ['db', 'Venue', 'Artist']
