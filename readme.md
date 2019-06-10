# Item Catalog

Web application that provides a list of items within a variety of categories.

## Getting Started

clone on download this repo to your local machine.

To clone, run:
```
https://github.com/akhilharihar/Udacity-Item-Catalog.git
```

or download the repo from [master.zip](https://github.com/akhilharihar/Udacity-Item-Catalog/archive/master.zip)


## Requirements

Item catalog is built on top of flask python microframework.
```
- Python3
- pip3
- Postgresql
- Nginx + Phusion Passenger Module
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