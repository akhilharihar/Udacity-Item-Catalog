#!/usr/bin/env bash

export DEBIAN_FRONTEND=noninteractive

ROOT_UID=0    
E_NOTROOT=87

CURRENT_USER=$USER
DB_NAME='catalog'

# Run as root, of course.
if [ "$UID" -ne "$ROOT_UID" ]
then
  echo "Must be root to run this script."
  exit $E_NOTROOT
fi

service postgres start

echo -n "Create postgres user for $CURRENT_USER (y/n)?"

read answer

if [ "$answer" != "${answer#[Yy]}" ];
then
    echo
    echo "--------------------------------------------"
    echo "Creating database user - catalog. Please enter a new password for user on prompt."
    echo "--------------------------------------------"
    sudo -u postgres createuser -D -A -P $CURRENT_USER
fi

echo -n "Create postgres database '$DB_NAME' (y/n)?"

read answer

if [ "$answer" != "${answer#[Yy]}" ];
then
    sudo -u postgres createdb -O $CURRENT_USER $DB_NAME
fi

apt-get -qq install libpq-dev

pip3 install -r requirements

npm install

if test -f "catalog.conf"; then
    echo "found nginx configuration file. Do you want to copy this configuration file to nginx?"
    
    read answer

    if [ "$answer" != "${answer#[Yy]}" ];
    then
        cp ./catalog.conf /etc/nginx/sites-enabled/catalog.conf
        nginx -t
    fi
else
    echo "creating catalog.conf file."
    cp ./catalog.conf.example ./catalog.conf
fi

if test -f ".env"; then
    echo "found .env file."
else
    echo "creating .env file file."
    cp ./.env.example ./.env
fi
