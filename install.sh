#!/usr/bin/env bash

echo
echo "--------------------------------------------"
echo "Install Catalog app dependencies"
echo "--------------------------------------------"
echo

export DEBIAN_FRONTEND=noninteractive

DB_NAME="catalog"

ROOT_UID=0    
E_NOTROOT=87


# Run as root, of course.
if [ "$UID" -ne "$ROOT_UID" ]
then
  echo "Must be root to run this script."
  exit $E_NOTROOT
fi

apt-get -qq update & apt-get upgrade

echo
echo "--------------------------------------------"
echo "Installing Prerequisites."
echo "--------------------------------------------"
echo

apt-get -qq install -y curl apt-transport-https ca-certificates dirmngr gnupg ufw

# Add passenger apt key
curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x561F9B9CAC40B2F7" | sudo apt-key add

sh -c 'echo deb https://oss-binaries.phusionpassenger.com/apt/passenger stretch main > /etc/apt/sources.list.d/passenger.list'

curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -

apt-get -qq update

apt-get -qq install -y python3 python3-pip nginx libnginx-mod-http-passenger postgresql postgresql-contrib nodejs

if [ ! -f /etc/nginx/modules-enabled/50-mod-http-passenger.conf ]
then 
    ln -s /usr/share/nginx/modules-available/mod-http-passenger.load /etc/nginx/modules-enabled/50-mod-http-passenger.conf ; 
fi

ls /etc/nginx/conf.d/mod-http-passenger.conf

echo
echo "--------------------------------------------"
echo "Creating database user - catalog. Please enter a new password for user on prompt."
echo "--------------------------------------------"

sudo -u postgres createuser -D -A -P $USER
sudo -u postgres createdb -O $USER $DB_NAME


echo
echo "--------------------------------------------"
echo "Configuring firewall. "
echo "--------------------------------------------"
echo

ufw allow ssh
ufw allow http
ufw allow https
ufw default allow outgoing
ufw default deny incoming

echo
echo "--------------------------------------------"
echo "Enabling system services"
echo "--------------------------------------------"
echo

systemctl enable nginx
echo "y" | sudo ufw enable
systemctl enable postgresql

exit 0