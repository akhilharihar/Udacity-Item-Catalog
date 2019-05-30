#!/usr/bin/env bash

echo
echo "--------------------------------------------"
echo "Setup Catalog app environment"
echo "--------------------------------------------"
echo

DB_USERNAME="catalog"
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

apt-get -qq install -y curl python3 python3-pip apt-transport-https ca-certificates 

apt-get -qq install -y dirmngr gnupg

# Add passenger apt key
curl -sL "http://keyserver.ubuntu.com/pks/lookup?op=get&search=0x561F9B9CAC40B2F7" | sudo apt-key add

sh -c 'echo deb https://oss-binaries.phusionpassenger.com/apt/passenger stretch main > /etc/apt/sources.list.d/passenger.list'

apt-get -qq update

echo
echo "--------------------------------------------"
echo "Installing nginx, passenger."
echo "--------------------------------------------"
echo

apt-get -qq install -y nginx ufw libnginx-mod-http-passenger

if [ ! -f /etc/nginx/modules-enabled/50-mod-http-passenger.conf ]
then 
    ln -s /usr/share/nginx/modules-available/mod-http-passenger.load /etc/nginx/modules-enabled/50-mod-http-passenger.conf ; 
fi

ls /etc/nginx/conf.d/mod-http-passenger.conf

echo
echo "--------------------------------------------"
echo "Installing postgresql."
echo "--------------------------------------------"
echo

apt-get -qq install -y postgresql postgresql-contrib

echo
echo "--------------------------------------------"
echo "Creating databse user - catalog. Please enter a new password on prompt."
echo "--------------------------------------------"

sudo -u postgres createuser -D -A -P $DB_USERNAME
sudo -u postgres createdb -O $DB_USERNAME $DB_NAME


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
systemctl enable ufw
systemctl enable postgresql

exit 0