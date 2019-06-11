# Item Catalog

Web application that provides a list of items within a category.

## Requirements

- Python > 3
- Postgresql > 9.6
- node.js

In production, you will also need to have
- nginx
- Phusion passenger

## Installation

Clone or [download](https://github.com/akhilharihar/Udacity-Item-Catalog/archive/master.zip) this repo to a directory.
```
git clone https://github.com/akhilharihar/Udacity-Item-Catalog.git
```
Rename .env.example to .env and fill in the required configuration. Refer [configuration](#configuration) section for more details.

Install dependencies
```
pip install -r requirements
npm install
```

Generate static assets dependencies
```
npm run dev
```

Migrate db schema to postgres database

```
flask db init
flask db migrate
flask db upgrade
```

To serve app:

```
flask run
```

To serve app with ssl:
```
flask run --cert=cert.pem --key=key.pem
```

If you do not have the data for category and item, please refer [database seeding](#database-seeding) section on how to add fake date for item and category.


## Deployment

Rename catalog.conf.example to catalog.conf and fill in the required configuration. Refer [nginx configuration](#nginx)

If you've spun up a new server for deployment, you can automate the installation of this project dependencies with the provided `install.sh` and `setup.sh` script files.

### Automated

The `install.sh` will install python3, nginx, passenger module, postgres, nodejs and setup firewall to only allow ssh, http and https ports. 

The `setup.sh` file will help you in creating a postgres user and database and add this application to nginx sites.

```
chmod +x install.sh
chmod +x setup.sh
sudo ./install.sh
sudo ./setup.sh
```

### Manual

Install nginx, libnginx-mod-http-passenger. Refer [https://www.phusionpassenger.com/docs/advanced_guides/install_and_upgrade/nginx/install/oss/stretch.html](https://www.phusionpassenger.com/docs/advanced_guides/install_and_upgrade/nginx/install/oss/stretch.html) on how to integrate phusion passenger with nginx.


Copy the catalog.conf to nginx sites directory. Usually, it is `/etc/nginx/sites-enabled/`

```
cp catalog.conf /etc/nginx/sites-enabled/catalog.conf
```

After copying, test if the configuration specified is correct.

```
nginx -t
```

Finally restart nginx for the changes to take effect.


## Configuration

### Environment

- **FLASk_ENV** - The environment the app is running in. values - development or production
- **APP_KEY** - Flask secret key. Please make sure that this value stays the same in production environment. Refer [secret key](http://flask.pocoo.org/docs/1.0/config/#SECRET_KEY).
- **SERVER_NAME** - The name and port of the server. eg: `127.0.0.1:5000, example.com`
- **STATIC_URL_PATH** - Used to specify a different path for the static files on the web. In development, this value does not effect the url of the static files. Refer [flask application object](http://flask.pocoo.org/docs/1.0/api/#application-object)
- **DB_URI** - Sqlalchemy database connection url - Refer [Sqlalchemy database urls](https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls).
- **USERS_SALT, CATEGORY_SALT, ITEM_SALT** - A random string to make hash of users, catgory, item id's unique. Please make sure that this value stays the same in production environment.
- **\*_CLIENT_ID, \*_CLIENT_SECRET** - Respective oauth providers client id and secret.

### Nginx

- **server_name** - Nginx virtual server name. eg: `example.com`. Refer [https://docs.nginx.com/nginx/admin-guide/web-server/web-server/#setting-up-virtual-servers](https://docs.nginx.com/nginx/admin-guide/web-server/web-server/#setting-up-virtual-servers)
- **passenger_python** - Absolute path to python version 3 interpreter. run `which python3` to know the path of python  interpreter in your system
- **root** - Absolute path to this application public directory. 

## Database Seeding

Open flask shell in terminal and run below commands.

```
from catalog.seeder import CategorySeeder, ItemSeeder

CategorySeeder.run(count=15)
ItemSeeder.run(count=100)
```

**count** - number of rows to insert to database