# THIS IS NOT READY YET! DO NOT USE... Thanks ;)

**To-Do:**

- [ ] Complete Seperate Function Files
- [ ] Take all function files and combine them into one menu
- [ ] Validate stuff works

Currently supports Ubuntu LTS

Self-Hosted Chatbot UI Installer by McKay Wrigley

This comprehensive menu-based installer is designed for individuals who wish to host their own chatbot UI on a cloud server instead of using Versal. It automates the installation and configuration process for all necessary components on your Ubuntu server. Before starting, please ensure that you have a VPS, SSH access, and a properly configured domain name (e.g., gpt.yourdomain) pointing to your VPS IP address. This is essential for SSL certificate issuance and proxy forwarding using Nginx and Certbot.

1. Install McKay Wrigley's Chatbot UI
2. Install Nginx
3. Configure Nginx
4. Install Certbot
5. Configure Certbot
6. Install Docker and Docker Compose
7. Configure Docker and Docker Compose settings
8. Install Custom Login Form
9. Configure Username and Password settings
10. Launch Chatbot UI


This installer simplifies the process of setting up your self-hosted chatbot UI, making it easier and more efficient.


# Setups for Installation:
1. sudo apt update
2. sudo apt upgrade
3. sudo apt install python3
4. sudo apt install python3-pip
5. pip3 install -r requirements.txt

# Start Menu

1. python3 menu.py
