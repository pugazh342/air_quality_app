# Import your application's Base and settings
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # Add project root to path
from app.db.database import Base
from app.db.models import * # Import all your models
from app.core.config import settings