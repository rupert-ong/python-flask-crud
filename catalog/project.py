from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)  # Pass in default file name as parameter


def create_db_session():
    """Connect to database and return session"""
    engine = create_engine('sqlite:///restaurantmenu.db', echo=True)
    Base.metadata.bind = engine

    db_session = sessionmaker(bind=engine)
    session = db_session()
    return session


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    """Make API endpoint for restaurant's menu items

        Args:
            restaurant_id:  Integer for restaurant table id
    """
    session = create_db_session()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menu_item_json(restaurant_id, menu_id):
    """Make API endpoint for individual menu item

        Args:
            restaurant_id:  Integer for restaurant tabe id
            menu_id:  Integer for menuItem table id
    """
    session = create_db_session()
    menu_item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(MenuItem=menu_item.serialize)


# Decorators for methods to execute based on route(s)
@app.route('/')
@app.route('/restaurants')
def restaurants():
    """Route for restaurants page"""
    session = create_db_session()
    items = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=items)


@app.route('/restaurants/new', methods=['GET', 'POST'])
def new_restaurant():
    """Route for new restaurant page"""
    if request.method == 'POST':
        new_item = Restaurant(name=request.form['name'])
        session = create_db_session()
        session.add(new_item)
        session.commit()
        flash("New restaurant created")
        return redirect(url_for('restaurants'))
    else:
        return render_template('newrestaurant.html')


@app.route('/restaurants/<int:restaurant_id>/edit', methods=['GET','POST'])
def edit_restaurant(restaurant_id):
    """Route for edit restaurant page

        Args:
            restaurant_id:  Integer for restaurant table id
    """
    session = create_db_session()
    edited_item = session.query(Restaurant).filter_by(id=restaurant_id).one()

    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        session.add(edited_item)
        session.commit()
        flash("Restaurant edited")
        return redirect(url_for('restaurants'))
    else:
        return render_template('editrestaurant.html', \
            restaurant_id=restaurant_id, restaurant=edited_item)


@app.route('/restaurants/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """Route for edit restaurant page

        Args:
            restaurant_id:  Integer for restaurant table id
    """
    session = create_db_session()
    deleted_item = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        flash("Restaurant deleted")
        return redirect(url_for('restaurants'))
    else:
        return render_template('deleterestaurant.html', \
            restaurant=deleted_item, \
            restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/menu')
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id):
    """Route for restaurant menu page

        Args:
            restaurant_id:  Integer for restaurant table id
    """
    session = create_db_session()
    restaurant = session.query(Restaurant).\
        filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).\
        filter_by(restaurant_id=restaurant.id).all()

    # Path queries into template so escape code has access to these variables
    return render_template('menu.html', restaurant=restaurant,
                           items=items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    """Route for new menu item for a restaurant page

        Args:
            restaurant_id:  Integer for restaurant table id
    """
    if request.method == 'POST':
        new_item = MenuItem(
            name=request.form['name'], description=request.form['description'],
            price=request.form['price'], course=request.form['course'],
            restaurant_id=restaurant_id)
        session = create_db_session()
        session.add(new_item)
        session.commit()
        flash("New menu item created")  # built in Flask messages (notifications)
        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    """Route for edit menu item for a restaurant page

        Args:
            restaurant_id:  Integer for restaurant table id
            menu_id: Integer for menu_item table id
    """
    session = create_db_session()
    edited_item = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        if request.form['name']:
            edited_item.name = request.form['name']
        if request.form['description']:
            edited_item.description = request.form['description']
        if request.form['price']:
            edited_item.price = request.form['price']
        if request.form['course']:
            edited_item.course = request.form['course']

        session.add(edited_item)
        session.commit()
        flash("Menu item edited")  # built in Flask messages (notifications)

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id,
                               menu_id=menu_id, item=edited_item)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    """Route for delete menu item for a restaurant page

        Args:
            restaurant_id:  Integer for restaurant table id
            menu_id: Integer for menu_item table id
    """
    session = create_db_session()
    deleted_item = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deleted_item)
        session.commit()
        flash("Menu item deleted")  # built in Flask messages (notifications)

        return redirect(url_for('restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id, menu_id=menu_id,
                               item=deleted_item)

# __main__ is the default name given to the application run by the Python
# interpreter. The below if statement only runs if this file is being executed
# by it explicitly. If it's imported, the below won't run
if __name__ == '__main__':
    app.secret_key = 'super_secret_key'  # For development purposes only
    app.debug = True  # Will reload automatically when code changes
    app.run(host='0.0.0.0', port=5000)  # Run on public IP, port 5000
