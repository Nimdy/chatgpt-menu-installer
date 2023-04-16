#!/bin/bash

function check_nginx_status() {
  sudo systemctl status nginx.service
}

function edit_domain_configuration() {
  read -rp "Enter your domain name (e.g., gpt.domain.com): " domain_name
  sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/"$domain_name"
  
  cat <<EOT | sudo tee /etc/nginx/sites-available/"$domain_name" >/dev/null
server {
    listen 80;
    listen [::]:80;
    server_name $domain_name;
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;

        proxy_buffering off; # Disable response buffering
    }
}
server {
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name $domain_name;
    ssl_certificate /etc/letsencrypt/live/$domain_name/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/$domain_name/privkey.pem;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_cache_bypass \$http_upgrade;

        proxy_buffering off; # Disable response buffering
    }
}

EOT

  sudo ln -s /etc/nginx/sites-available/"$domain_name" /etc/nginx/sites-enabled/
  sudo rm /etc/nginx/sites-enabled/default
}

function verify_nginx_config() {
  sudo nginx -t
}

function restart_nginx() {
  sudo systemctl restart nginx.service
}

function check_ufw_status() {
  ufw_status=$(sudo ufw status | grep -w "Status")
  if [[ "$ufw_status" == "Status: active" ]]; then
    sudo ufw allow 'Nginx HTTPS'
  fi
}

echo "Checking Nginx service status..."
check_nginx_status

echo "Editing domain configuration..."
edit_domain_configuration

echo "Verifying Nginx configuration..."
verify_nginx_config

nginx_test_result=$(verify_nginx_config 2>&1)
if [[ "$nginx_test_result" == *"failed"* ]]; then
  echo "Nginx configuration test failed. Please check the configuration and try again."
else
  echo "Restarting Nginx to apply new configurations..."
  restart_nginx

  echo "Checking UFW status and allowing Nginx HTTPS if necessary..."
  check_ufw_status
fi
