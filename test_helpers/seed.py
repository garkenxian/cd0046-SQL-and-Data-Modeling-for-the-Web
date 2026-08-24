"""Database seeding helper functions."""

from dal import db, Venue, Artist

def seed_database():
    """Seed database with test data."""
    # Clear existing data
    db.session.query(Venue).delete()
    db.session.query(Artist).delete()

    # Add test venues
    venue1 = Venue(
        name='The Musical Hop',
        city='San Francisco',
        state='CA',
        address='1015 Folsom Street',
        phone='123-123-1234',
        website='https://www.themusicalhop.com',
        facebook_link='https://www.facebook.com/TheMusicalHop',
        image_link='https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60'
    )

    venue2 = Venue(
        name='The Dueling Pianos Bar',
        city='New York',
        state='NY',
        address='335 Delancey Street',
        phone='914-003-1132',
        website='https://www.theduelingpianos.com',
        facebook_link='https://www.facebook.com/theduelingpianos',
        image_link='https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80'
    )

    venue3 = Venue(
        name='Park Square Live Music & Coffee',
        city='San Francisco',
        state='CA',
        address='34 Whiskey Moore Ave',
        phone='415-000-1234',
        website='https://www.parksquarelivemusicandcoffee.com',
        facebook_link='https://www.facebook.com/ParkSquareLiveMusicAndCoffee',
        image_link='https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80'
    )

    # Add test artists
    artist1 = Artist(
        name='Guns N Petals',
        city='San Francisco',
        state='CA',
        phone='326-123-5000',
        genres='Rock n Roll',
        facebook_link='https://www.facebook.com/GunsNPetals',
        image_link='https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80'
    )

    artist2 = Artist(
        name='Matt Quevedo',
        city='New York',
        state='NY',
        phone='300-400-5000',
        genres='Jazz',
        facebook_link='https://www.facebook.com/mattquevedo923251523',
        image_link='https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80'
    )

    artist3 = Artist(
        name='The Wild Sax Band',
        city='San Francisco',
        state='CA',
        phone='432-325-5432',
        genres='Jazz, Classical',
        facebook_link='https://www.facebook.com/thewildsaxband',
        image_link='https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80'
    )

    # Add to database
    db.session.add_all([venue1, venue2, venue3])
    db.session.add_all([artist1, artist2, artist3])

    try:
        db.session.commit()
        return True, '✅ Database seeded successfully!'
    except Exception as e:
        db.session.rollback()
        return False, f'❌ Error seeding database: {e}'
