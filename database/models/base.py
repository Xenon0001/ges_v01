"""
Base model for all GES entities
"""

from sqlalchemy.ext.declarative import declarative_base

# Single Base for all models to avoid relationship issues
Base = declarative_base()
