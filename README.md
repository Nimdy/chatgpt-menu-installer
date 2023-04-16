# THIS IS NOT READY YET! DO NOT USE... Thanks ;)

**To-Do:**

- [ ] Complete Seperate Function Files
- [ ] Take all function files and combine them into one menu
- [ ] Validate stuff works

Currently supports Ubuntu LTS




![image](https://user-images.githubusercontent.com/16698453/232345507-fa2c9c9d-69f9-4415-bda3-ec5b6adce580.png)



My login plugin


![image](https://user-images.githubusercontent.com/16698453/232345653-6792b639-0652-4cd1-8d27-5e8dd9affaba.png)



Self-Hosted Chatbot UI Installer by McKay Wrigley

This comprehensive menu-based installer is designed for individuals who wish to host their own chatbot UI on a cloud server instead of using Versal. It automates the installation and configuration process for all necessary components on your Ubuntu server. Before starting, please ensure that you have a VPS, SSH access, and a properly configured domain name (e.g., gpt.yourdomain) pointing to your VPS IP address. This is essential for SSL certificate issuance and proxy forwarding using Nginx and Certbot.

1. Installs McKay Wrigley's Chatbot UI
2. Installs Nginx
3. Configures Nginx
4. Installs Certbot
5. Configures Certbot
6. Installs Docker and Docker Compose
7. Configures Docker and Docker Compose
8. Installs Custom Login Form on demand
9. Remove Custom Login Form on demand
10. Configures envorimental variables:
11. Checks McKay Wrigley's Chatbot UI for updates and updates it.
```
OPENAI_API_KEY if no input leave var blank
OPENAI_API_HOST if no input enter https://api.openai.com
OPENAI_API_TYPE if no input enter openai
OPENAI_API_VERSION if not input enter 2023-03-15-preview
AZURE_DEPLOYMENT_ID if no input leave var blank
OPENAI_ORGANIZATION if no input leave var blank
DEFAULT_MODEL if no input enter gpt-3.5-turbo	
NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT if not input enter You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.
GOOGLE_API_KEY if no input leave var blank
GOOGLE_CSE_ID if no input leave var blank
```
11. Launches Chatbot UI


This installer simplifies the process of setting up your self-hosted chatbot UI, making it easier and more efficient.


# Setups for Installation:
1. sudo apt update
2. sudo apt upgrade
3. sudo apt install python3
4. sudo apt install python3-pip
5. pip3 install -r requirements.txt

# Start Menu

1. python3 menu.py
