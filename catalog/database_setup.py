# Configuration code
import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# Class Code
class Restaurant(Base):
    # Table Info
    __tablename__ = 'restaurant'

    # Mapper
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class MenuItem(Base):
    __tablename__ = 'menu_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)


# End of File
# What db do we want to communicate with...
engine = create_engine('sqlite:///restaurantmenu.db')

# Bind engine to the Base class
Base.metadata.create_all(engine)
