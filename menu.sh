#!/bin/bash

function main_menu() {
  clear
  echo "------------------------------------"
  echo "  GPT Chatbot Installation Script"
  echo "------------------------------------"
  echo "1. Update & Upgrade System"
  echo "2. Install Docker, Docker Compose & Git"
  echo "3. Configure Nginx"
  echo "4. Setup SSL with Certbot"
  echo "5. Setup GPT Chatbot UI"
  echo "6. Add Nimdys Login Form"
  echo "7. Exit"
  echo ""
}

function pause() {
  read -rp "Press [Enter] key to continue..."
}

while true; do
  main_menu
  read -rp "Enter your choice [1-6]: " choice

  case $choice in
    1)
      sudo apt update
      sudo apt upgrade
      echo "System Updated & Upgraded"
      pause
      ;;
    2)
      sudo apt install docker docker-compose
      sudo apt install git

      wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
      sudo mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
      sudo chmod -v +x /usr/local/bin/docker-compose

      sudo systemctl enable docker.service
      sudo systemctl start docker.service
      sudo usermod -a -G docker ubuntu

      sudo apt install nginx

      pause
      ;;
    3)
      source configure_nginx.sh

      pause
      ;;
    4)
      source setup_ssl.sh

      pause
      ;;
    5)
      source setup_gpt_chatbot.sh

      pause
      ;;
      
    6)
      add_login_form_plugin.sh
      
      pause
      ;;
    7)
      echo "Exiting..."
      exit 0
      ;;
    *)
      echo "Invalid option, please try again."
      pause
      ;;
  esac
done
