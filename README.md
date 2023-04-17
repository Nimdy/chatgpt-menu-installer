# Self-Hosted Chatbot UI Installer

Note: This project is currently in development and not ready for production use. Please use it for testing purposes only.

This comprehensive menu-based installer is designed for individuals who wish to host their own chatbot UI on a cloud server instead of using Versal. It automates the installation and configuration process for all necessary components on your Ubuntu server.

Before starting, please ensure that you have a VPS, SSH access, and a properly configured domain name (e.g., gpt.yourdomain) pointing to your VPS IP address. This is essential for SSL certificate issuance and proxy forwarding using Nginx and Certbot.

## Why not SHORTER COMMANDS>?!?!?!

Like all of my menu-based installers, this one includes additional steps that could potentially be condensed into one-liner commands. However, my intention in designing these installers is to assist individuals who are new to Linux and are in the process of learning. By providing a more detailed and step-by-step approach, I aim to help users understand the correct procedures before introducing them to shortcuts. I appreciate your understanding and kindness as you use this installer. :)

## Features
- Installs McKay Wrigley's Chatbot UI
- Installs and configures Nginx
- Installs and configures Certbot
- Installs and configures Docker and Docker Compose
- Installs Custom Login Form on demand
- Removes Custom Login Form on demand
- Configures environment variables
- Checks for updates to McKay Wrigley's Chatbot UI and applies them
- Launches Chatbot UI

**To-Do:**

- [X] Complete Seperate Function Files
- [X] Take all function files and combine them into one menu
- [ ] Validate functionality
- [ ] Improve user interface design
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

3. Edit the sudoers file:
```
visudo
```
- Add the following line:
```
UserNameYouWant ALL=(ALL:ALL) ALL
```

4. Save file and continue


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

## Start Menu
To start the installation menu, run the following command:
```
python3 menu.py
```




![image](https://user-images.githubusercontent.com/16698453/232345507-fa2c9c9d-69f9-4415-bda3-ec5b6adce580.png)



My login plugin


![image](https://user-images.githubusercontent.com/16698453/232345653-6792b639-0652-4cd1-8d27-5e8dd9affaba.png)

## Disclaimer
This project is currently in development and is intended for testing purposes only. Please use caution when using it on a production server. The project currently supports Ubuntu LTS, and testing on other platforms is pending.
