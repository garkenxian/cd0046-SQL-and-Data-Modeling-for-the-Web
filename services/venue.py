"""
Business logic layer for venue-related operations.
"""
from dal.venue import Venue
from dto.venue import VenueDTO
from dal import db

class VenueService():
    @staticmethod
    def get_venues_grouped_by_location():
        """Get all venues grouped by city and state.
        
        Returns a list of dictionaries with structure:
        [{
            "city": "San Francisco",
            "state": "CA",
            "venues": [{"id": 1, "name": "...", "num_upcoming_shows": 0}, ...]
        }, ...]
        """
        # TODO: num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
        
        venues = Venue.query.all()
        
        # Group venues by city and state
        grouped = {}
        for venue in venues:
            key = (venue.city, venue.state)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(venue)
        
        # Transform into expected format
        data = []
        for (city, state), venue_list in grouped.items():
            venues_formatted = [{
                "id": v.id,
                "name": v.name,
                "num_upcoming_shows": 0  # TODO: count upcoming shows when Show model is available
            } for v in venue_list]
            
            data.append({
                "city": city,
                "state": state,
                "venues": venues_formatted
            })
        
        return data

    @staticmethod
    def show_venue_by_venue_id(venue_id):
        data1={
            "id": 1,
            "name": "The Musical Hop",
            "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
            "address": "1015 Folsom Street",
            "city": "San Francisco",
            "state": "CA",
            "phone": "123-123-1234",
            "website": "https://www.themusicalhop.com",
            "facebook_link": "https://www.facebook.com/TheMusicalHop",
            "seeking_talent": True,
            "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
            "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
            "past_shows": [{
                "artist_id": 4,
                "artist_name": "Guns N Petals",
                "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
                "start_time": "2019-05-21T21:30:00.000Z"
            }],
            "upcoming_shows": [],
            "past_shows_count": 1,
            "upcoming_shows_count": 0,
            }
        data2={
            "id": 2,
            "name": "The Dueling Pianos Bar",
            "genres": ["Classical", "R&B", "Hip-Hop"],
            "address": "335 Delancey Street",
            "city": "New York",
            "state": "NY",
            "phone": "914-003-1132",
            "website": "https://www.theduelingpianos.com",
            "facebook_link": "https://www.facebook.com/theduelingpianos",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
            "past_shows": [],
            "upcoming_shows": [],
            "past_shows_count": 0,
            "upcoming_shows_count": 0,
            }
        data3={
            "id": 3,
            "name": "Park Square Live Music & Coffee",
            "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
            "address": "34 Whiskey Moore Ave",
            "city": "San Francisco",
            "state": "CA",
            "phone": "415-000-1234",
            "website": "https://www.parksquarelivemusicandcoffee.com",
            "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
            "seeking_talent": False,
            "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
            "past_shows": [{
                "artist_id": 5,
                "artist_name": "Matt Quevedo",
                "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
                "start_time": "2019-06-15T23:00:00.000Z"
            }],
            "upcoming_shows": [{
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-01T20:00:00.000Z"
            }, {
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-08T20:00:00.000Z"
            }, {
                "artist_id": 6,
                "artist_name": "The Wild Sax Band",
                "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
                "start_time": "2035-04-15T20:00:00.000Z"
            }],
            "past_shows_count": 1,
            "upcoming_shows_count": 1,
            }
        data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
        return data

    @staticmethod
    def search_venue_by_name(search_term):

        # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
        # seach for Hop should return "The Musical Hop".
        # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

        st = search_term

        return {
            "count": 1,
            "data": [
                {
                    "id": 2,
                    "name": "The Dueling Pianos Bar",
                    "num_upcoming_shows": 0,
                }
            ]
        }

    def validate_venue_form_data(form_data):
        validation_error = None
        data = VenueDTO(
            name = form_data['name']
        )
        ## return validation_error, data
        return validation_error, data

    @staticmethod
    def create_venue(venue_dto:VenueDTO):
        return True, None

    @staticmethod
    def update_venue(venue_id:int, venue_dto:VenueDTO):
        try:
            # Find the venue
            venue = Venue.query.get(venue_id)
            if not venue:
                return False, f"Venue with id {venue_id} not found"
            
            # Update venue fields
            venue.name = venue_dto.name
            # TODO: Update other fields when DTO is fully implemented
            
            # Commit changes
            db.session.commit()
            
            return True, None
        except Exception as e:
            from dal import db
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def delete_venue(venue_id:any):
        # TODO: Complete this endpoint for taking a venue_id, and using
        # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
        return True