from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem


def createDBSession():
    """Connect to database and return session"""
    engine = create_engine('sqlite:///restaurantmenu.db', echo=True)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

app = Flask(__name__)  # Pass in default file name as parameter


# Decorators for methods to execute based on route(s)
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    session = createDBSession()
    restaurant = session.query(Restaurant).\
        filter(Restaurant.id == restaurant_id).one()
    items = session.query(MenuItem).\
        filter(MenuItem.restaurant_id == restaurant.id).all()
    output = ""

    for item in items:
        output += ("<p><strong>%s</strong><br>%s<br>%s</p>") % (
            item.name, item.price, item.description)

    return output

# __main__ is the default name given to the application run by the Python
# interpreter. The below if statement only runs if this file is being executed
# by it explicitly. If it's imported, the below won't run
if __name__ == '__main__':
    app.debug = True  # Will reload automatically when code changes
    app.run(host='0.0.0.0', port=5000)  # Run on public IP, port 5000
