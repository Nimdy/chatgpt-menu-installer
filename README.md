# Self-Hosted Chatbot UI Installer

This product is finally ready for test and use. 100% works on a fresh Ubuntu Server with a Domain Name assigned to the IP address and is validated through DNS.

![image](https://user-images.githubusercontent.com/16698453/235796586-16773e6b-6631-4ade-a93f-5c619caa1931.png)

## Server Hosting Provided By DigitalOcean
* https://m.do.co/c/9d2217a2725c
* Use my link and get 100 USD Server Credits from me,  over the next 60 Days!
* Free Credits without hacks... 

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

## Pre-Chatbot UI Installation Steps

1. Update the package list:
```
sudo apt update
```

2. Upgrade installed packages:
```
sudo apt upgrade
```

3. Install Python 3:
```
sudo apt install python3
```

4. Install pip for Python 3:
```
sudo apt install python3-pip
```

5. Reboot System
```
sudo reboot
```

## After the system reboots login with your new user account you created before continuing

6. Clone this repo in the /opt directory and assign ownership to your user - Do not use root for this step
```
cd /opt
sudo git clone https://github.com/Nimdy/chatgpt-menu-installer.git
sudo chown -R $USER:$USER /chatgpt-menu-installer/
```

7. Change into the new cloned repo director.
```
cd chatgpt-menu-installer
```

8. Install required Python packages:
```
sudo pip3 install -r requirements.txt
```
## Now you are ready to start the menu. Time to go for a ride! 

9. Start the menu:
To start the installation menu, run the following command with sudo
```
python3 menu.py
```

10. Start the Chatbot UI Installation
Press 2 for the Chatbot UI Installation Menu option

11. Install Nginx Server
Press y to install Nginx

12. Enter your domain name
Press y to enter your domain name 

13. Restart Nginx 
If the configuration is verified press y to restart Nginx

14. Setup Certbot
Press y to install Certbot

15. Enter your Certbot Details
email address, domain name, and press y to agree to terms

16. After Certbot is installed, press y to restart Nginx

17. Docker will now install. After the docker installation is complete, you need to logout and log back in 

18. After logging out and logging back in, launch the menu again and press 2 to continue the Chatbot UI installation. The installation will continue where you left off.
```
cd /opt/chatgpt-menu-installer
```

19. Switch back to root and then back to your account you created at the very start of the installation


20. Launch menu again
```
python3 menu.py
```

21. Press 2 and continue the install of Chatbot UI by McKay Wrigley - the script will continue where you left off because of the docker security and workflow in this design

22. Download and Install Chatbot UI
Press y to download and install Chatbot UI

23. Enter your API Key information for OpenAI and Google Analytics etc... Press enter to use the default values if you do not have an API key for the service
Press y to continue and save the API Key information

24. Agree to overwrite the .env.local file with your new information
Press y to continue

25. Press y to build the Chatbot UI Docker Image
This will take a few minutes to complete the build and after it is complete, the Chatbot UI will be active and ready for use on your domain name.
https://yourdomain.com

## From this point forward you are all setup and ready to go. If you wish to install the Login Form, please continue with the steps below.

1. Open the menu once more

2. Select option 3 to initiate the Login Form installation

3. Press 'y' to confirm the installation

4. Provide the desired JWT Username and Password for the Login Form, and indicate if you'd like to bypass it

5. Input a random string of characters for the JWT Secret Key, which is essential for encrypting the JWT Token and ensuring the Login Form functions correctly

6. Review the provided information and press 'y' to proceed

7. Press 'y' to rebuild the Chatbot UI Docker Image, incorporating the Login Form

8. The script will prompt you to choose a domain name from a list of configured domains on your server. Select the one you'd like to use for the Login Form

9. The script will then configure the NGINX Server and add location blocks for JWT API calls

10. Once the NGINX Server Configurations are updated, the script will restart NGINX, and your Chatbot UI will be ready for use with the Login Form

## If you do a docker ps you should see this:

![image](https://user-images.githubusercontent.com/16698453/235796145-eae4ae68-71da-4a16-9989-c5df1ca3de70.png)

## Disclaimer
This project is currently in development and is intended for testing purposes only. Please use caution when using it on a production server. The project currently supports Ubuntu LTS, and testing on other platforms is pending.
