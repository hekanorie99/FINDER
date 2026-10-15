"""phone-osint — legal OSINT toolkit for phone numbers."""
from .core import investigate
from .models import PhoneReport

__version__ = "0.1.0"
__all__ = ["investigate", "PhoneReport"]
