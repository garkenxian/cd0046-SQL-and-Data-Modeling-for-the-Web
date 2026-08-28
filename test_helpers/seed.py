"""Database seeding helper functions."""

from datetime import datetime
from dal import db, Venue, Artist, Show
from dal.genre import Genre


def seed_database():
    """Seed database with test data.
    
    Process:
    1. Create and commit Genre objects (PostgreSQL auto-generates IDs)
    2. Create Venue objects with genre relationships
    3. Create Artist objects with genre relationships
    4. Commit venues and artists (SQLAlchemy inserts into junction tables)
    5. Create Show objects with venue and artist foreign keys
    6. Commit shows
    """
    try:
        # Clear existing data (in reverse order of dependencies)
        db.session.query(Show).delete()
        db.session.query(Artist).delete()
        db.session.query(Venue).delete()
        db.session.query(Genre).delete()
        db.session.commit()

        # Step 1: Create and commit genres first (no manual IDs)
        genres_data = [
            'Jazz', 'Reggae', 'Swing', 'Classical', 'Folk',
            'Rock n Roll', 'R&B', 'Hip-Hop'
        ]
        genres_dict = {}
        for genre_name in genres_data:
            genre = Genre(name=genre_name)
            genres_dict[genre_name] = genre
            db.session.add(genre)
        
        db.session.commit()

        # Step 2 & 3: Create venues and artists with genre relationships (no manual IDs)
        venue1 = Venue(
            name='The Musical Hop',
            city='San Francisco',
            state='CA',
            address='1015 Folsom Street',
            phone='123-123-1234',
            website='https://www.themusicalhop.com',
            facebook_link='https://www.facebook.com/TheMusicalHop',
            image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60',
            seeking_talent=True,
            seeking_description='We are on the lookout for a local artist to play every two weeks. Please call us.'
        )
        venue1.genres.extend([genres_dict['Jazz'], genres_dict['Reggae'], genres_dict['Swing'], genres_dict['Classical'], genres_dict['Folk']])

        venue2 = Venue(
            name='The Dueling Pianos Bar',
            city='New York',
            state='NY',
            address='335 Delancey Street',
            phone='914-003-1132',
            website='https://www.theduelingpianos.com',
            facebook_link='https://www.facebook.com/theduelingpianos',
            image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80',
            seeking_talent=False,
            seeking_description=''
        )
        venue2.genres.extend([genres_dict['Classical'], genres_dict['R&B'], genres_dict['Hip-Hop']])

        venue3 = Venue(
            name='Park Square Live Music & Coffee',
            city='San Francisco',
            state='CA',
            address='34 Whiskey Moore Ave',
            phone='415-000-1234',
            website='https://www.parksquarelivemusicandcoffee.com',
            facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
            image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80',
            seeking_talent=False,
            seeking_description=''
        )
        venue3.genres.extend([genres_dict['Rock n Roll'], genres_dict['Jazz'], genres_dict['Classical'], genres_dict['Folk']])

        artist1 = Artist(
            name='Guns N Petals',
            city='San Francisco',
            state='CA',
            phone='326-123-5000',
            website='https://www.gunsnpetalsband.com',
            facebook_link='https://www.facebook.com/GunsNPetals',
            image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80',
            seeking_venue=True,
            seeking_description='Looking for shows to perform at in the San Francisco Bay Area!'
        )
        artist1.genres.append(genres_dict['Rock n Roll'])

        artist2 = Artist(
            name='Matt Quevedo',
            city='New York',
            state='NY',
            phone='300-400-5000',
            website='',
            facebook_link='https://www.facebook.com/mattquevedo923251523',
            image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80',
            seeking_venue=False,
            seeking_description=''
        )
        artist2.genres.append(genres_dict['Jazz'])

        artist3 = Artist(
            name='The Wild Sax Band',
            city='San Francisco',
            state='CA',
            phone='432-325-5432',
            website='',
            facebook_link='https://www.facebook.com/thewildsaxband',
            image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80',
            seeking_venue=False,
            seeking_description=''
        )
        artist3.genres.extend([genres_dict['Jazz'], genres_dict['Classical']])

        # Add venues and artists to session, then commit
        # SQLAlchemy will handle junction table inserts via the relationships
        db.session.add_all([venue1, venue2, venue3])
        db.session.add_all([artist1, artist2, artist3])
        db.session.commit()

        # Step 4: Create shows with ForeignKey references to venues and artists
        # SQLAlchemy will automatically use the committed IDs
        show1 = Show(
            venue_id=venue1.id,
            artist_id=artist1.id,
            start_time=datetime(2019, 5, 21, 21, 30, 0)
        )

        show2 = Show(
            venue_id=venue3.id,
            artist_id=artist2.id,
            start_time=datetime(2019, 6, 15, 23, 0, 0)
        )

        show3 = Show(
            venue_id=venue3.id,
            artist_id=artist3.id,
            start_time=datetime(2035, 4, 1, 20, 0, 0)
        )

        show4 = Show(
            venue_id=venue3.id,
            artist_id=artist3.id,
            start_time=datetime(2035, 4, 8, 20, 0, 0)
        )

        show5 = Show(
            venue_id=venue3.id,
            artist_id=artist3.id,
            start_time=datetime(2035, 4, 15, 20, 0, 0)
        )

        # Add and commit shows
        db.session.add_all([show1, show2, show3, show4, show5])
        db.session.commit()
        
        return True, '✅ Database seeded successfully!'
    except Exception as e:
        db.session.rollback()
        return False, f'❌ Error seeding database: {e}'
