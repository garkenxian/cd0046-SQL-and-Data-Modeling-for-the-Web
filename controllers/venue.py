from flask import Blueprint, render_template, request, flash, redirect, url_for
from forms import VenueForm
from services.venue import VenueService

venue_bp = Blueprint('venues', __name__, url_prefix='/venues')

@venue_bp.route('/', strict_slashes=False)
def venues():
    data = VenueService.get_venues_grouped_by_location()
    return render_template('pages/venues.html', areas=data)

@venue_bp.route('/search', methods=['POST'])
def search_venues():
    response = VenueService.search_venue_by_name(request.form.get('search_term', ''))
    return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@venue_bp.route('/<int:venue_id>')
def show_venue(venue_id):
    data = VenueService.show_venue_by_venue_id(venue_id=venue_id)
    return render_template('pages/show_venue.html', venue=data)

@venue_bp.route('/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)

@venue_bp.route('/create', methods=['POST'])
def create_venue_submission():
    form = VenueForm()
    validation_error, venue_data = VenueService.validate_venue_form_data(request.form)
    
    if validation_error:
        flash(f"Form validation failed: {validation_error}", category='error')
        return render_template('forms/new_venue.html', form=form, error=validation_error, data=request.form)
    
    venue_create_success, venue_fail_reason = VenueService.create_venue(venue_data)
    
    if venue_create_success:
        flash(f"Venue {venue_data.name} was successfully listed!", category='success')
        return redirect(url_for('venues.venues', _external=False))
    else:
        flash(f"Venue could not be listed: {venue_fail_reason}", category='error')
        return render_template('forms/new_venue.html', form=form, error=venue_fail_reason, data=request.form)

@venue_bp.route('/<int:venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    result = VenueService.delete_venue(venue_id=venue_id)  

    if result:
        return {'success': True, 'message': 'Venue deleted successfully!'}, 200
    else:
        return {'success': False, 'message': 'Unable to delete venue'}, 400

@venue_bp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    # Loads the Venue Data to edit
    form = VenueForm()
    data = VenueService.show_venue_by_venue_id(venue_id=venue_id)
    
    # Populate form with venue data
    form.name.data = data.get('name')
    form.city.data = data.get('city')
    form.state.data = data.get('state')
    form.address.data = data.get('address')
    form.phone.data = data.get('phone')
    form.image_link.data = data.get('image_link')
    form.genres.data = data.get('genres', [])
    form.facebook_link.data = data.get('facebook_link')
    form.website_link.data = data.get('website')
    form.seeking_talent.data = data.get('seeking_talent', False)
    form.seeking_description.data = data.get('seeking_description')
    
    return render_template('forms/edit_venue.html', form=form, venue=data)

@venue_bp.route('/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    form = VenueForm()
    validation_error, venue_data = VenueService.validate_venue_form_data(request.form)
    
    if validation_error:
        flash(f"Form validation failed: {validation_error}", category='error')
        return render_template('forms/edit_venue.html', form=form, error=validation_error, data=request.form)
    
    venue_edit_success, venue_fail_reason = VenueService.update_venue(venue_id, venue_data)
    
    if venue_edit_success:
        flash(f"Venue {venue_data.name} was successfully updated!", category='success')
        return redirect(url_for('venues.show_venue', venue_id=venue_id))
    else:
        flash(f"Venue could not be updated: {venue_fail_reason}", category='error')
        return render_template('forms/edit_venue.html', form=form, error=venue_fail_reason, data=request.form)

