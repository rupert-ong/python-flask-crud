# Python Flask CRUD Application

**Python Flask CRUD Application** is a persistent Python based CRUD application using the [Flask](http://flask.pocoo.org) framework. This project is written in [Python](https://www.python.org), [SQLAlchemy](http://sqlalchemy.org) and [SQLite](https://www.sqlite.org).


This side project can be found in the Fullstack Foundations course at [Udacity](https://www.udacity.com), under "Developing with Frameworks"

## Table of contents

* [Quick start](#quick-start)
* [What's included](#whats-included)
* [Contributors](#contributors)
* [Copyright and license](#copyright-and-license)


## Quick start

Here's what you need to do to view this project:

1. Install [Vagrant](https://www.vagrantup.com) and [VirtualBox](https://www.virtualbox.org).
2. Within Terminal (Mac), navigate to the root directory of this project and launch the Vagrant VM by running the command `vagrant up`.
3. SSH into the running Vagrant machine `vagrant ssh`. 
4. Run `cd/vagrant/catalog` to change directory.
5. Run `python database_setup.py` to create the database.
6. Run `python menu_populator.py` to populate it.
7. Finally, run `python project.py` to start the web server.
8. Open your browser and navigate to `http://localhost:5000`


### What's included

Within the downloaded files, this is the relevant structure:

```
python-web-server-crud/
├── Vagrantfile
└── pg_config.sh
    └── catalog/
        └── static
            └── styles.css
        └── templates
            ├── deletemenuitem.html
            ├── deleterestaurant.html
            ├── editmenuitem.html
            ├── editrestaurant.html
            ├── menu.html
            ├── newmenuitem.html
            ├── newrestaurant.html
            └── restaurants.html
        ├── database_setup.py
        ├── menu_populator.py
        └── project.py
```

## Contributors

**Rupert Ong**

* <https://twitter.com/rupertong>
* <https://github.com/rupert-ong>


## Copyright and license

Code and documentation copyright 2011-2016 Udacity Inc. All rights reserved.
