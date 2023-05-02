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

![image](https://user-images.githubusercontent.com/16698453/235570661-a41f2154-a398-4eb5-bb23-adff9cd59259.png)

```
python3 menu.py
```
10. Press 2 to install Chatbot UI

11. Accept any defaults

12. Install Nginx Server

![image](https://user-images.githubusercontent.com/16698453/235570854-0586cc5b-e98c-4e82-95c8-cfde1434cf38.png)

13. Press Y to add a new domain

![image](https://user-images.githubusercontent.com/16698453/235570940-573af654-88d6-4bb3-b2ea-2619371e8f19.png)

14. Enter Domain Name

![image](https://user-images.githubusercontent.com/16698453/235571012-96108502-4b67-4f99-975d-b16b923efc2b.png)

15. Restart Nginx

![image](https://user-images.githubusercontent.com/16698453/235571040-f80caac3-1902-4b3d-aa8c-51c59b71012d.png)

16. Setup Certbot

![image](https://user-images.githubusercontent.com/16698453/235571073-a6442e72-b76a-415c-8b19-fc5773d81631.png)

17. Enter your Certbot Details

![image](https://user-images.githubusercontent.com/16698453/235571175-afba789d-d0d3-4f0b-946e-6607f7011963.png)

18. Agree to auto or not

![image](https://user-images.githubusercontent.com/16698453/235571305-ba73a1ea-ee45-4b18-a26f-5a7d55cf5bb9.png)

19. Complete Certbot with Defaults or your own picks

20. Docker will start to install and finish. Press "N" for no and stop install 

![image](https://user-images.githubusercontent.com/16698453/235571447-26531d90-2e76-470a-8f9c-bca73fd1c80a.png)

21. Switch back to root and then back to your account you created at the very start of the installation

![image](https://user-images.githubusercontent.com/16698453/235571634-3e82d53b-68d9-4365-8212-aa7a313f0e86.png)

22. Launch menu again
```
python3 menu.py
```

23. Press 2 and continue the install of Chatbot UI by McKay Wrigley - the script will continue where you left off because of the docker security and workflow in this design

![image](https://user-images.githubusercontent.com/16698453/235571779-22dd736c-5c7b-436a-a636-13ff93ea8350.png)

24. Enter your Variables as needed and if you agree press Y

![image](https://user-images.githubusercontent.com/16698453/235571870-c81be659-ad5a-46a5-9cbe-e06774429a9c.png)

25. Over write the .env.local file with your new variable information

![image](https://user-images.githubusercontent.com/16698453/235571939-9c3ca447-df11-4c50-b65a-bb3a57842c04.png)

26. Checks to verify Docker is part of your group, press Y

![image](https://user-images.githubusercontent.com/16698453/235572009-197bba82-07c5-4348-bea7-ab015a947d97.png)

27. Switch to root and then back to your user (might be a dup action, I can fix later)

![image](https://user-images.githubusercontent.com/16698453/235572153-f4c8751a-a283-4ae9-bdc8-b98446412ea9.png)

28. Open the menu again and press 2 to continue with the install

![image](https://user-images.githubusercontent.com/16698453/235572312-75acd70d-ffa2-4327-a73e-6cb110600bf5.png)

29. Yes I have a dup function... Continue with the same variable input and continue. Chatbot UI will now download and install. Wait for it to finish

![image](https://user-images.githubusercontent.com/16698453/235572572-3f591d72-a3c1-424b-ad1b-3f0cdd23cf90.png)

30. ChatbotUI is fully optional now

![image](https://user-images.githubusercontent.com/16698453/235572717-bc4a56cd-7ea5-45f1-ba9c-4557b3ab890b.png)

31. Add my login form if you wish by pressing 3

![image](https://user-images.githubusercontent.com/16698453/235572771-d0234044-3c3c-4f9d-b667-42f082ea480a.png)

I have added Formik and Axios to the ChatbotUI package.json file

32. Enter your username and password for login. Enter your Bypass login or not. Enter your JWT Secret Key for auth tokens

![image](https://user-images.githubusercontent.com/16698453/235572994-4b2f1597-eaf8-41a8-a194-1a78d928c2b7.png)

33. Say yes to rebuilding the ChatbotUI Docker Image. This is going to take the LoginForm, _app.tsx and auth.ts files and rebuild the Docker Image. Wait for it to finish.

![image](https://user-images.githubusercontent.com/16698453/235573045-f805ea2c-a402-4071-b913-b9aea8b2a08d.png)

![image](https://user-images.githubusercontent.com/16698453/235573422-b7b91f4d-be5c-44e5-a9c5-7356558cd4d2.png)


34. Select your domain name:

![image](https://user-images.githubusercontent.com/16698453/235573523-c39352d9-c9d0-4370-b400-d9d598f3fc3c.png)















## Disclaimer
This project is currently in development and is intended for testing purposes only. Please use caution when using it on a production server. The project currently supports Ubuntu LTS, and testing on other platforms is pending.
