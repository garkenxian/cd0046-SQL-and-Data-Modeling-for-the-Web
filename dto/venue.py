from dataclasses import dataclass
from typing import Optional

@dataclass
class VenueDTO:
    id: Optional[int]
    name: str
    city: str
    state: str
    address: str
    phone: str
    image_link: str
    facebook_link: str
    website: str