# Self-Hosted Chatbot UI Installer

This product is finally ready for test and use. 100% works on a fresh Ubuntu Server with a Domain Name assigned to the IP address and is validated through DNS.

## Ready for Testing
Installation script works 100% - On a clean VPS with the VPS domain name assigned to a public IP - 5/1/2023 2130 MST

This comprehensive menu-based installer is designed for individuals who wish to host their own chatbot UI on a cloud server instead of using Versal. It automates the installation and configuration process for all necessary components on your Ubuntu server.

Before starting, please ensure that you have a VPS, SSH access, and a properly configured domain name (e.g., gpt.yourdomain) pointing to your VPS IP address. This is essential for SSL certificate issuance and proxy forwarding using Nginx and Certbot.

## Why not SHORTER COMMANDS>?!?!?!

Like all of my menu-based installers, this one includes additional steps that could potentially be condensed into one-liner commands. However, my intention in designing these installers is to assist individuals who are new to Linux and are in the process of learning. By providing a more detailed and step-by-step approach, I aim to help users understand the correct procedures before introducing them to shortcuts. I appreciate your understanding and kindness as you use this installer. :)

## Features
- Installs McKay Wrigley's Chatbot UI
- Installs and configures Nginx
- Installs and configures Certbot
- Installs and configures Docker and Docker Compose
- Configures environment variables
- Configures HTTPS SSL/TLS Certs for your domain
- Checks for updates to McKay Wrigley's Chatbot UI and applies them
- Launches Chatbot UI

## On demand Features for Login Form install:
1. Builds another Docker Image for Node and JSON Web Token to handle authenication
2. Add LoginForm to components/Settings/LoginForm.tsx 
3. Replace pages/_app.tsx and with code needed for interaction with LoginForm.tsx
4. Create utils/app/auth.ts for storing and removing access session token
5. Adds axios and formik to package.json
6. Rebuilds ChatbotUI Docker Image and implements required changes for Login Form function.

## Steps:
1. Updates and Upgrades VPS
2. Install Nginx
3. Takes input for the domain you wish to have
4. Configures Nginx based on your domain name settings and proxy forwards 3000(Chatbot UI) to 443(Public Facing Access)
5. Installs Certbot
6. Takes your cert details and configures them to Nginx
7. Downloads Mckay Wrigley's Chatbot UI
8. Takes your VAR inputs for API keys and Prompts - Defaults if no input is provided
9. Builds ChatbotUI Docker Image based on input
10. Starts Docker Image and is ready for interactions
11. Install Nimdy's Login Form
12. Builds Docker Image for JSON Web Token and Node configuration ports
13. Rebuilds ChatbotUI Docker Image with Login Form and JWT
14. Rebuilds NGINX Server Configurations and adds JWT API call location blocks
15. Starts all services and is ready for interactions



**To-Do:**

- [X] Complete Seperate Function Files
- [X] Take all function files and combine them into one menu
- [X] Validate functionality
- [ ] Validate plugin install
- [ ] Add ability to load and unload plugins on demand

## Compatibility

Currently supports Ubuntu LTS (testing on other platforms is pending).

## Server Hosting Provided By DigitalOcean

- https://m.do.co/c/9d2217a2725c
- Use my link and get 100 USD Server Credits from me,  over the next 60 Days!
- Free Credits without hacks... 

## Initial Setup for a Blank VPS Pre-Pre Setup

If you are using a blank VPS, please create a non-root user first:

1. Create a new user:
```
sudo adduser UserNameYouWant
```

2. Add the new user to the sudo group:
```
usermod -aG sudo UserNameYouWant
```

3. Switch to UserNameYouWant
```
su UserNameYouWant
```

## Configure your domain name
Make sure your domain name is pointing to your VPS IP address. 
```
https://docs.digitalocean.com/tutorials/dns-registrars/
```

## Installation Steps

1. Update the package list:
```
sudo apt update
```

2. Upgrade installed packages:
```
sudo apt upgrade
```

3. Reboot System
```
sudo reboot
```

## After the system reboots login with your new user account you created before continuing

4. Install Python 3:
```
sudo apt install python3
```

5. Install pip for Python 3:
```
sudo apt install python3-pip
```

6. Clone this repo
```
git clone https://github.com/Nimdy/chatgpt-menu-installer.git
```

7. Change into the new cloned repo director.
```
cd chatgpt-menu-installer
```

8. Install required Python packages:
```
pip3 install -r requirements.txt
```
## Now you are ready to start the menu. Time to go for a ride! 

9. Start the menu:
To start the installation menu, run the following command:
```
python3 menu.py

10. Press 2 to install Chatbot UI

11. Accept the 



![image](https://user-images.githubusercontent.com/16698453/232345507-fa2c9c9d-69f9-4415-bda3-ec5b6adce580.png)



My login plugin


![image](https://user-images.githubusercontent.com/16698453/232345653-6792b639-0652-4cd1-8d27-5e8dd9affaba.png)

## Disclaimer
This project is currently in development and is intended for testing purposes only. Please use caution when using it on a production server. The project currently supports Ubuntu LTS, and testing on other platforms is pending.
