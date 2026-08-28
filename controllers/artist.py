#TODO: Search that is empty needs to show an error and then return to the referrer
from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import ArtistForm
from services.artist import ArtistService

artist_bp = Blueprint('artists', __name__, url_prefix='/artists')

# GET /artists
@artist_bp.route('/', strict_slashes=False)
def artists():
    """Display all artists.
    
    Returns a page with all artists in the database.
    """
    data = ArtistService.get_all_artists()
    return render_template('pages/artists.html', artists=data)

# POST /artists/search
@artist_bp.route('/search', methods=['POST'])
def search_artists():
    """Search artists by name.
    
    Accepts a search term from form data and returns matching artists.
    Returns the search results page with the search term and results.
    """
    search_term = request.form.get('search_term', '').strip()

    if not search_term:
        flash("Please enter a valid search term", category='error')
        return redirect(request.referrer or url_for('artists.artists'))
    
    response = ArtistService.search_artist_by_name(search_term=search_term)
    return render_template('pages/search_artists.html', results=response, search_term=search_term)

# GET /artists/:artist_id
@artist_bp.route('/<int:artist_id>')
def show_artist(artist_id):
    """Display details for a specific artist.
    
    Takes artist_id as URL parameter and returns the artist detail page
    with all information about that artist. Redirects back if artist not found.
    """
    data = ArtistService.show_artist_by_artist_id(artist_id=artist_id)
    
    if not data:
        flash(f"Artist with ID {artist_id} not found", category='error')
        return redirect(request.referrer or url_for('artists.artists'))
    
    return render_template('pages/show_artist.html', artist=data)

# GET /artists/create
@artist_bp.route('/create', methods=['GET'])
def create_artist_form():
    """Display the form to create a new artist.
    
    Returns the artist creation form for user to fill out.
    """
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form, data={})

# POST /artists/create
@artist_bp.route('/create', methods=['POST'])
def create_artist_submission():
    """Handle artist creation form submission.
    
    Validates the form data, creates the artist in the database,
    and redirects to the artists list on success or redisplays the form on error.
    """
    form = ArtistForm()
    validation_error, artist_data = ArtistService.validate_artist_form_data(request.form)
    
    if validation_error:
        flash(f"Form validation failed: {validation_error}", category='error')
        return render_template('forms/new_artist.html', form=form, error=validation_error, data=request.form)
    
    artist_create_success, artist_fail_reason = ArtistService.create_artist(artist_data)
    
    if artist_create_success:
        flash(f"Artist {artist_data.name} was successfully listed!", category='success')
        return redirect(url_for('artists.artists', _external=False))
    else:
        flash(f"Artist could not be listed: {artist_fail_reason}", category='error')
        return render_template('forms/new_artist.html', form=form, error=artist_fail_reason, data=request.form)

# GET /artists/:artist_id/edit
@artist_bp.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    """Display the form to edit an existing artist.
    
    Takes artist_id as URL parameter, fetches the artist data from the database,
    and returns a form pre-populated with the current artist information.
    """
    form = ArtistForm()
    data = ArtistService.show_artist_by_artist_id(artist_id=artist_id)
    
    if not data:
        flash(f"Artist with ID {artist_id} not found", category='error')
        return redirect(request.referrer or url_for('artists.artists'))
    
    # Populate form with artist data
    form.name.data = data.get('name')
    form.city.data = data.get('city')
    form.state.data = data.get('state')
    form.phone.data = data.get('phone')
    form.image_link.data = data.get('image_link')
    form.genres.data = data.get('genres', [])
    form.facebook_link.data = data.get('facebook_link')
    form.website_link.data = data.get('website')
    form.seeking_venue.data = data.get('seeking_venue', False)
    form.seeking_description.data = data.get('seeking_description')
    
    return render_template('forms/edit_artist.html', form=form, artist=data)

# DELETE /artists/:artist_id
@artist_bp.route('/<int:artist_id>', methods=['DELETE'])
def delete_artist(artist_id):
    """Delete an artist by its ID.
    
    Takes artist_id as URL parameter and deletes that artist from the database.
    Returns a JSON response with success or failure status.
    """
    result = ArtistService.delete_artist(artist_id=artist_id)

    if result:
        return {'success': True, 'message': 'Artist deleted successfully!'}, 200
    else:
        return {'success': False, 'message': 'Unable to delete artist'}, 400

# POST /artists/:artist_id/edit
@artist_bp.route('/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    """Handle artist edit form submission.
    
    Takes artist_id as URL parameter, validates the submitted form data,
    updates the artist in the database, and redirects on success
    or redisplays the form on error.
    """
    form = ArtistForm()
    artist = ArtistService.show_artist_by_artist_id(artist_id=artist_id)
    
    if not artist:
        flash(f"Artist with ID {artist_id} not found", category='error')
        return redirect(request.referrer or url_for('artists.artists'))
    
    validation_error, artist_data = ArtistService.validate_artist_form_data(request.form)
    
    if validation_error:
        flash(f"Form validation failed: {validation_error}", category='error')
        return render_template('forms/edit_artist.html', form=form, artist=artist, error=validation_error)
    
    artist_edit_success, artist_fail_reason = ArtistService.update_artist(artist_id, artist_data)
    
    if artist_edit_success:
        flash(f"Artist {artist_data.name} was successfully updated!", category='success')
        return redirect(url_for('artists.show_artist', artist_id=artist_id))
    else:
        flash(f"Artist could not be updated: {artist_fail_reason}", category='error')
        return render_template('forms/edit_artist.html', form=form, artist=artist, error=artist_fail_reason)
