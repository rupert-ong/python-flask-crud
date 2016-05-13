import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Class Code
class Restaurant(Base):
    """Declarative base class for Restaurant Table

        Args:
            Base: Declarative base instance from SQLAlchemy

    """

    __tablename__ = 'restaurant'


    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class MenuItem(Base):
    """Declarative base class for MenuItem table

        Args:
            Base: Declarative base instance from SQLAlchemy
    """

    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


    @property
    def serialize(self):
        """Send JSON objects in a serializable format

            Args:
                self
        """
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course
        }


# End of File
# What db do we want to communicate with...
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind engine to the Base class
Base.metadata.create_all(engine)
