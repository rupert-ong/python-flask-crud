from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)  # Pass in default file name as parameter


def createDBSession():
    """Connect to database and return session"""
    engine = create_engine('sqlite:///restaurantmenu.db', echo=True)
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session


# Decorators for methods to execute based on route(s)
@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
    session = createDBSession()
    restaurant = session.query(Restaurant).\
        filter(Restaurant.id == restaurant_id).one()
    items = session.query(MenuItem).\
        filter(MenuItem.restaurant_id == restaurant.id).all()

    # Path queries into template so escape code has access to these variables
    return render_template('menu.html', restaurant=restaurant,
                           items=items)


@app.route('/restaurant/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "Page to create a new menu item."


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "Page to edit a menu item."


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "Page to delete a menu item."

# __main__ is the default name given to the application run by the Python
# interpreter. The below if statement only runs if this file is being executed
# by it explicitly. If it's imported, the below won't run
if __name__ == '__main__':
    app.debug = True  # Will reload automatically when code changes
    app.run(host='0.0.0.0', port=5000)  # Run on public IP, port 5000
