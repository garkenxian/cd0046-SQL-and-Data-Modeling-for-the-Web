# Albums & Songs Showcase Implementation Plan

## Overview
Add the ability for artists to list their albums and songs on their artist profile page. This is a "Stand Out" feature that enhances the platform by allowing artists to showcase their music.

---

## Database Schema

### 1. Album Model
**File:** `dal/album.py`

```python
class Album(db.Model):
    __tablename__ = 'album'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    release_date = db.Column(db.Date)
    description = db.Column(db.Text)
    image_link = db.Column(db.String)  # Album cover art
    spotify_link = db.Column(db.String)  # Link to Spotify album
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    artist = db.relationship('Artist', backref='albums')
    songs = db.relationship('Song', backref='album', cascade='all, delete-orphan')
```

### 2. Song Model
**File:** `dal/song.py`

```python
class Song(db.Model):
    __tablename__ = 'song'
    
    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.Integer)  # Duration in seconds
    track_number = db.Column(db.Integer)  # Track position on album
    genre = db.Column(db.String(120))
    spotify_track_id = db.Column(db.String)
    spotify_link = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
```

### 3. Update Artist Model
**File:** `dal/artist.py` (already has backref via Album.artist)

No changes needed - Album relationship is automatically created via the backref in Album model.

---

## DTOs (Data Transfer Objects)

### 1. AlbumDTO
**File:** `dto/album.py`

```python
from typing import List, Optional
from datetime import date, datetime

class SongDTO:
    def __init__(self, id=None, title='', duration=0, track_number=None, 
                 genre='', spotify_link=''):
        self.id = id
        self.title = title
        self.duration = duration
        self.track_number = track_number
        self.genre = genre
        self.spotify_link = spotify_link

class AlbumDTO:
    def __init__(self, id=None, artist_id=None, title='', release_date=None,
                 description='', image_link='', spotify_link='', songs=None):
        self.id = id
        self.artist_id = artist_id
        self.title = title
        self.release_date = release_date
        self.description = description
        self.image_link = image_link
        self.spotify_link = spotify_link
        self.songs = songs or []
```

---

## Service Layer

### 1. AlbumService
**File:** `services/album.py`

```python
class AlbumService:
    @staticmethod
    def get_albums_by_artist(artist_id: int) -> List[AlbumDTO]:
        """Get all albums for an artist, sorted by release_date (newest first)."""
        
    @staticmethod
    def get_album_with_songs(album_id: int) -> AlbumDTO:
        """Get album details including all songs."""
        
    @staticmethod
    def create_album(album_dto: AlbumDTO) -> tuple:
        """Create new album. Returns (success, error_message)."""
        
    @staticmethod
    def update_album(album_id: int, album_dto: AlbumDTO) -> tuple:
        """Update existing album. Returns (success, error_message)."""
        
    @staticmethod
    def delete_album(album_id: int) -> tuple:
        """Delete album and cascade delete songs. Returns (success, error_message)."""
        
    @staticmethod
    def validate_album_form_data(form_data) -> tuple:
        """Validate album form data. Returns (validation_errors_dict, album_dto)."""
```

### 2. SongService
**File:** `services/song.py`

```python
class SongService:
    @staticmethod
    def get_songs_by_album(album_id: int) -> List[SongDTO]:
        """Get all songs for an album, sorted by track_number."""
        
    @staticmethod
    def create_song(song_dto: SongDTO) -> tuple:
        """Create new song. Returns (success, error_message)."""
        
    @staticmethod
    def update_song(song_id: int, song_dto: SongDTO) -> tuple:
        """Update existing song. Returns (success, error_message)."""
        
    @staticmethod
    def delete_song(song_id: int) -> tuple:
        """Delete song. Returns (success, error_message)."""
```

---

## Forms

### 1. AlbumForm
**File:** `forms.py`

```python
class AlbumForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    release_date = DateField('release_date', validators=[Optional()])
    description = TextAreaField('description', validators=[Optional()])
    image_link = StringField('image_link', 
        validators=[OptionalURL(require_tld=True, message='Album cover must be a valid URL')])
    spotify_link = StringField('spotify_link',
        validators=[OptionalURL(require_tld=True, message='Spotify link must be a valid URL')])
```

### 2. SongForm
**File:** `forms.py`

```python
class SongForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    track_number = IntegerField('track_number', validators=[Optional()])
    duration = IntegerField('duration', validators=[Optional()])  # in seconds
    genre = StringField('genre', validators=[Optional()])
    spotify_link = StringField('spotify_link',
        validators=[OptionalURL(require_tld=True, message='Spotify link must be a valid URL')])
```

---

## Controllers

### 1. AlbumController
**File:** `controllers/album.py`

Routes to implement:
- `GET /artists/<artist_id>/albums` - List all albums for an artist
- `GET /albums/<album_id>` - View album details with songs
- `GET /albums/create` - Show create album form
- `POST /albums/create` - Create new album
- `GET /albums/<album_id>/edit` - Edit album form
- `POST /albums/<album_id>/edit` - Update album
- `POST /albums/<album_id>/delete` - Delete album

### 2. SongController
**File:** `controllers/song.py`

Routes to implement:
- `POST /albums/<album_id>/songs` - Create song in album
- `GET /songs/<song_id>/edit` - Edit song
- `POST /songs/<song_id>/edit` - Update song
- `POST /songs/<song_id>/delete` - Delete song

---

## Templates

### 1. Album List
**File:** `templates/pages/artist_albums.html`

```html
<!-- Shows in artist profile or separate page -->
<section>
  <h2>Albums</h2>
  <div class="albums-grid">
    {% for album in artist.albums %}
    <div class="album-card">
      <img src="{{ album.image_link }}" alt="{{ album.title }}">
      <h4>{{ album.title }}</h4>
      <p>{{ album.release_date|datetime('long') }}</p>
      <p>{{ album.songs|length }} songs</p>
      <a href="/albums/{{ album.id }}" class="btn btn-primary">View Album</a>
      <a href="/albums/{{ album.id }}/edit" class="btn btn-secondary">Edit</a>
    </div>
    {% endfor %}
  </div>
  <a href="/albums/create?artist_id={{ artist.id }}" class="btn btn-success">Add Album</a>
</section>
```

### 2. Album Detail with Songs
**File:** `templates/pages/album.html`

```html
<div class="album-header">
  <img src="{{ album.image_link }}" alt="{{ album.title }}" class="album-cover">
  <div class="album-info">
    <h1>{{ album.title }}</h1>
    <p>By <a href="/artists/{{ album.artist_id }}">{{ album.artist.name }}</a></p>
    <p>Released: {{ album.release_date|datetime('long') }}</p>
    <p>{{ album.description }}</p>
    {% if album.spotify_link %}
    <a href="{{ album.spotify_link }}" class="btn btn-success" target="_blank">
      Listen on Spotify
    </a>
    {% endif %}
  </div>
</div>

<section>
  <h2>Tracklist</h2>
  <table class="songs-table">
    <thead>
      <tr>
        <th>#</th>
        <th>Title</th>
        <th>Duration</th>
        <th>Genre</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      {% for song in album.songs %}
      <tr>
        <td>{{ song.track_number or '-' }}</td>
        <td>
          {% if song.spotify_link %}
          <a href="{{ song.spotify_link }}" target="_blank">{{ song.title }}</a>
          {% else %}
          {{ song.title }}
          {% endif %}
        </td>
        <td>{{ (song.duration / 60)|int }}:{{ '%02d'|(song.duration % 60) }}</td>
        <td>{{ song.genre }}</td>
        <td>
          <a href="/songs/{{ song.id }}/edit" class="btn btn-sm">Edit</a>
          <form method="post" action="/songs/{{ song.id }}/delete" style="display:inline;">
            <button type="submit" class="btn btn-sm btn-danger">Delete</button>
          </form>
        </td>
      </tr>
      {% endfor %}
    </tbody>
  </table>
  <a href="/albums/{{ album.id }}/songs/create" class="btn btn-success">Add Song</a>
</section>
```

---

## Integration Points

### 1. Update Artist Profile
Modify `templates/pages/show_artist.html` to include an "Albums" section:

```html
<section>
  <h2>Albums & Music</h2>
  {% if artist.albums %}
    <div class="albums-preview">
      {% for album in artist.albums|slice(4) %} <!-- Show first 4 albums -->
      <div class="album-preview">
        <img src="{{ album.image_link }}" alt="{{ album.title }}">
        <h5>{{ album.title }}</h5>
        <p>{{ album.songs|length }} songs</p>
        <a href="/albums/{{ album.id }}">View Album</a>
      </div>
      {% endfor %}
    </div>
    <a href="/artists/{{ artist.id }}/albums">View All Albums</a>
  {% else %}
    <p>No albums yet</p>
    <a href="/albums/create?artist_id={{ artist.id }}" class="btn btn-primary">
      Add Your First Album
    </a>
  {% endif %}
</section>
```

---

## Database Migrations

Create migration files using Flask-Migrate:

```bash
# Generate migration
flask db migrate -m "Add Album and Song models"

# Review generated migration file and adjust if needed

# Apply migration
flask db upgrade
```

---

## Implementation Sequence

1. **Phase 1 - Models & DTOs**
   - Create `dal/album.py` with Album model
   - Create `dal/song.py` with Song model
   - Create `dto/album.py` with AlbumDTO and SongDTO
   - Update Artist model relationships

2. **Phase 2 - Services**
   - Create `services/album.py` with AlbumService
   - Create `services/song.py` with SongService
   - Implement all CRUD operations
   - Add validation logic

3. **Phase 3 - Forms**
   - Add AlbumForm and SongForm to `forms.py`
   - Include proper validation (URLs, required fields)

4. **Phase 4 - Controllers & Routes**
   - Create `controllers/album.py`
   - Create `controllers/song.py`
   - Implement all routes with proper error handling
   - Support query parameters for prepopulating artist/album

5. **Phase 5 - Templates**
   - Create `templates/pages/artist_albums.html`
   - Create `templates/pages/album.html`
   - Create `templates/forms/new_album.html`
   - Create `templates/forms/new_song.html`
   - Update `templates/pages/show_artist.html`

6. **Phase 6 - Database Migrations**
   - Run Flask-Migrate to create schema changes
   - Test migrations with fresh database

7. **Phase 7 - Testing**
   - Write unit tests for AlbumService
   - Write unit tests for SongService
   - Write integration tests for routes
   - Aim for 80%+ coverage on new code

8. **Phase 8 - Styling & UX**
   - Add CSS for album grid layout
   - Add responsive design for mobile
   - Implement album cover image display

---

## Optional Enhancements

1. **Bulk Song Import** - Import songs from CSV or Spotify API
2. **Album Stats** - Track plays, favorites, reviews
3. **Public Playlists** - Allow fans to create playlists from songs
4. **Genre Tags** - Track genre per song and album
5. **Duration Stats** - Calculate total album duration
6. **Release Calendar** - Show upcoming album releases
7. **Spotify Sync** - Auto-sync albums/songs from artist's Spotify profile

---

## Technical Considerations

### Data Validation
- Album title: Required, max 255 chars
- Song title: Required, max 255 chars
- Duration: Optional, positive integer (seconds)
- Track number: Optional, positive integer
- Dates: Use ISO 8601 format
- URLs: Must be valid HTTP/HTTPS URLs with domain

### Cascade Deletes
- Deleting album cascade-deletes all songs in that album
- Deleting artist does NOT automatically delete albums (manual review required)

### Relationships
- One Artist → Many Albums (1:M)
- One Album → Many Songs (1:M)
- Songs cannot exist without an Album

### Performance
- Eager-load songs when fetching album details
- Paginate album lists for artists with many albums
- Cache popular albums/songs if performance needed

---

## Error Handling

- "Album not found" when accessing non-existent album
- "Artist not found" when accessing non-existent artist
- Validation errors for missing required fields
- Duplicate title prevention (artist cannot have two albums with same title)
- Cannot add song to non-existent album

---

## User Flow

### Creating an Album
1. Artist visits their profile page
2. Clicks "Add Album" button
3. Fills in album details (title, release date, cover image, description)
4. Submits form
5. System creates album and redirects to album page
6. Artist can now add songs to the album

### Adding Songs to Album
1. Artist views album page
2. Clicks "Add Song"
3. Fills in song details (title, track number, duration, genre, Spotify link)
4. Submits form
5. Song is added to album and displays in tracklist

### Viewing an Album
1. User visits artist profile
2. Sees albums preview
3. Clicks on album to view full details
4. Sees complete tracklist with links to Spotify
5. Can listen directly via Spotify embeds/links

---

## Success Criteria

✅ Artists can create albums  
✅ Artists can add songs to albums  
✅ Album information displays on artist profile  
✅ Users can view album details and tracklists  
✅ Songs link to Spotify for listening  
✅ Proper validation and error messages  
✅ Database cascades handle deletions correctly  
✅ Unit tests achieve 80%+ coverage  
✅ UI is responsive and user-friendly  

