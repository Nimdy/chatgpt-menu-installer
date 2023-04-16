#!/bin/bash

function install_certbot() {
  sudo apt update
  sudo apt install certbot python3-certbot-nginx -y
}

function setup_ssl_certificate() {
  read -rp "Enter your domain name (e.g., gpt.domain.com): " domain_name
  sudo certbot --nginx -d "$domain_name"
}

function configure_auto_renewal() {
  read -rp "Do you want to configure automatic certificate renewal? (y/n): " auto_renewal
  if [ "$auto_renewal" == "y" ] || [ "$auto_renewal" == "Y" ]; then
    (crontab -l 2>/dev/null; echo "0 5 * * * /usr/bin/certbot renew --quiet") | crontab -
  fi
}

echo "Installing Certbot and Nginx plugin..."
install_certbot

echo "Setting up SSL certificate for your domain..."
setup_ssl_certificate

echo "Configuring automatic certificate renewal..."
configure_auto_renewal
