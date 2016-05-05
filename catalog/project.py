from flask import Flask, render_template, request, redirect, url_for
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
        filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).\
        filter_by(restaurant_id=restaurant.id).all()

    # Path queries into template so escape code has access to these variables
    return render_template('menu.html', restaurant=restaurant,
                           items=items)


@app.route('/restaurant/<int:restaurant_id>/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(
            name=request.form['name'], description=request.form['description'],
            price=request.form['price'], course=request.form['course'],
            restaurant_id=restaurant_id)
        session = createDBSession()
        session.add(newItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    session = createDBSession()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()

    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        if request.form['description']:
            editedItem.description = request.form['description']
        if request.form['price']:
            editedItem.price = request.form['price']
        if request.form['course']:
            editedItem.course = request.form['course']

        session.add(editedItem)
        session.commit()

        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editmenuitem.html', restaurant_id=restaurant_id,
                               menu_id=menu_id, item=editedItem)


@app.route('/restaurant/<int:restaurant_id>/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    session = createDBSession()
    deletedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template('deletemenuitem.html',
                               restaurant_id=restaurant_id, menu_id=menu_id,
                               item=deletedItem)

# __main__ is the default name given to the application run by the Python
# interpreter. The below if statement only runs if this file is being executed
# by it explicitly. If it's imported, the below won't run
if __name__ == '__main__':
    app.debug = True  # Will reload automatically when code changes
    app.run(host='0.0.0.0', port=5000)  # Run on public IP, port 5000
