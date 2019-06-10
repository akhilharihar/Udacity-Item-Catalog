# Item Catalog

Web application that provides a list of items within a variety of categories.

## Getting Started

clone on download this repo to your local machine.

To clone, run:
```
git clone https://github.com/akhilharihar/Udacity-Item-Catalog.git
```

or download the repo from [master.zip](https://github.com/akhilharihar/Udacity-Item-Catalog/archive/master.zip)


## Requirements

Item catalog is built on top of flask python microframework.
```
- Python3
- pip3
- Postgresql
- Nginx + Phusion Passenger Module
- npm
```

## Development

Rename .env.example to .env and Fill all the details.

```
pip install -r requirements
npm run dev
```

To serve the app:

```
flask run
```

Unfortunately, facebook oauth does not work under http. Workaround is to generate and install a self signed certificate for 127.0.0.1.

to run flask app with ssl

```
flask run --cert=cert.pem --key=key.pem
```

## Deployment.

You can manually install the above tools or use the install.sh file included along with this project to install all dependencies.

To use the dependency installer, run:

```
chmod +x install.sh
sudo ./install.sh
```

Then run:
```
chmod +x setup.sh
sudo ./setup.sh
```

The setup file will help you in creating a postgres user under current linux user name and database with name 'catalog'. To change the database user name and database name, edit the `CURRENT_USER`, `DB_NAME` variables in setup.sh file.

The setup file will create .env and nginx site conf file. Complete the details in the .env, catalog.conf file and restart nginx for the changes to take effect.

Finally run the below command to generate application static assets.

In development: 
```
npm run dev
```
static assets are generated in ./app/static directory

In production:
```
npm run prod
```
static assets are generated in ./public directory.