#!/usr/bin/env python3
import os
import getpass
import subprocess
import requests
import shutil
import socket
import re
import time
import tempfile
import getpass
import grp
import curses
from termcolor import colored

domain_name = None

def read_progress_file(progress_filename):
    if os.path.exists(progress_filename):
        with open(progress_filename, "r") as f:
            return int(f.read().strip())
    return 0

def update_progress_file(progress_filename, step):
    with open(progress_filename, "w") as f:
        f.write(str(step))

def main_installation_function():
    progress_filename = "installation_progress.txt"
    saved_step = read_progress_file(progress_filename)

    if saved_step > 0:
        print(f"Continuing installation from step {saved_step}.")
        response = get_user_response("Do you want to continue from the saved step? (y/n): ")

        if not response:
            response = get_user_response("Do you want to start with a fresh install? (y/n): ")
            if not response:
                print("Aborted installation.")
                return
            saved_step = 0

    # Initialize curses
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)

    try:
        # Divide the screen into two parts
        top_win = curses.newwin(5, curses.COLS, 0, 0)
        bottom_win = curses.newwin(curses.LINES - 5, curses.COLS, 5, 0)

        def update_step_status(step):
            top_win.clear()
            for i in range(1, step):
                top_win.addstr(1, 2 + (i - 1) * 15, f"[✓] Step {i}")
            top_win.addstr(1, 2 + (step - 1) * 15, f"[✗] Step {step}")
            top_win.refresh()

        if saved_step < 1:
            update_step_status(1)
            step1_update_and_upgrade_system(bottom_win)
            update_progress_file(progress_filename, 1)

        if saved_step < 2:
            update_step_status(2)
            step2_configure_nginx(bottom_win)
            update_progress_file(progress_filename, 2)

        if saved_step < 3:
            update_step_status(3)
            step3_setup_ssl_certbot(bottom_win)
            update_progress_file(progress_filename, 3)

        if saved_step < 4:
            update_step_status(4)
            step4_install_docker_docker_compose_git(bottom_win)
            update_progress_file(progress_filename, 4)

        if saved_step < 5:
            update_step_status(5)
            step5_setup_gpt_chatbot_ui(bottom_win)
            update_progress_file(progress_filename, 5)

        # Add more steps as needed if you want to customize the installation process

    finally:
        # Clean up curses
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

    # Remove the progress file once the installation is complete
    if os.path.exists(progress_filename):
        os.remove(progress_filename)

def save_domain_name_to_file():
    with open("domain_name.txt", "w") as f:
        f.write(domain_name)

def load_domain_name_from_file():
    global domain_name

    try:
        with open("domain_name.txt", "r") as f:
            domain_name = f.read().strip()
    except FileNotFoundError:
        print(colored("Domain name not found. It will be set during the Nginx configuration process.", "red"))

def get_user_response(prompt, bottom_win):
    while True:
        bottom_win.addstr(prompt)
        bottom_win.refresh()
        response = bottom_win.getstr().strip().decode("utf-8").lower()

        if response in ['y', 'n']:
            bottom_win.addstr("\n")
            bottom_win.refresh()
            return response == 'y'
        else:
            bottom_win.addstr("Invalid input. Please enter 'y' or 'n'.\n")
            bottom_win.refresh()



def safe_system_call(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def step1_update_and_upgrade_system(bottom_win):
    print(colored("Updating the package list...", "cyan"))
    os.system("sudo apt-get update")

    print(colored("Upgrading the system...", "cyan"))
    os.system("sudo apt-get upgrade -y")

    print(colored("Cleaning up unused packages...", "cyan"))
    os.system("sudo apt-get autoremove -y")

    print(colored("System update and upgrade completed.", "green"))
    print(colored("Please reboot the system to apply the changes.", "green"))
    print(colored("After rebooting, run this script again to continue with menu option 2.", "green"))

def create_new_user():
    while True:
        new_username = input(colored("Enter a new username: ", "yellow")).strip()
        if not new_username:
            print(colored("Username cannot be empty. Please try again.", "red"))
            continue

        exists = subprocess.run(f"getent passwd {new_username}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if exists:
            print(colored("The provided username already exists. Please try another username.", "red"))
            continue
        else:
            break

    password = getpass.getpass(colored(f"Enter the password for {new_username}: ", "yellow"))
    confirm_password = getpass.getpass(colored(f"Confirm the password for {new_username}: ", "yellow"))

    while password != confirm_password:
        print(colored("Passwords don't match. Please try again.", "red"))
        password = getpass.getpass(colored(f"Enter the password for {new_username}: ", "yellow"))
        confirm_password = getpass.getpass(colored(f"Confirm the password for {new_username}: ", "yellow"))

    encrypted_password = subprocess.check_output(f"openssl passwd -1 {password}", shell=True, text=True).strip()

    os.system(f"sudo useradd -m -p {encrypted_password} {new_username}")
    os.system(f"sudo usermod -aG sudo {new_username}")
    print(colored(f"User {new_username} created with sudo permissions.", "green"))
    return new_username

def check_nginx_running():
    try:
        output = subprocess.check_output("systemctl is-active nginx", shell=True)
        return output.strip().decode("utf-8") == "active"
    except subprocess.CalledProcessError:
        return False

def is_domain_publicly_visible(domain_name):
    try:
        domain_ip = socket.gethostbyname(domain_name)
        public_ip = requests.get("https://api64.ipify.org").text
        return domain_ip == public_ip, public_ip
    except Exception as e:
        print(f"Error: {e}")
        return False, None

def step2_configure_nginx(bottom_win):
    global domain_name
    print("Configuring Nginx...")

    if not check_nginx_running():
        if get_user_response("Nginx is not running. Do you want to install and start Nginx? (y/n): "):
            print("Installing Nginx...")
            os.system("sudo apt-get install -y nginx")
            print("Starting Nginx...")
            os.system("sudo systemctl start nginx")
        else:
            print("Please install and start Nginx before configuring.")
            return

    if not get_user_response("Do you want to add a new domain to the Nginx configuration? (y/n): "):
        print("Aborted Nginx configuration.")
        return

    domain_name = input("Enter the domain name (e.g., gpt.domain.com) where your GPT bot will be hosted: ")

    domain_visible, ip_address = is_domain_publicly_visible(domain_name)
    if not domain_visible:
        print(f"Warning: The domain name {domain_name} either does not resolve in the global DNS or does not resolve to the public IP address. This might cause issues with Certbot.")
    else:
        print(f"The domain name {domain_name} is publicly visible and resolves to IP address {ip_address}.")
        save_domain_name_to_file()

    if not domain_visible:
        if not get_user_response("Do you want to continue with the configuration? (y/n): "):
            print("Aborted Nginx configuration.")
            return
 
    nginx_config = f"""
server {{
    listen 80;
    listen [::]:80;
    server_name {domain_name};
    location / {{
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_buffering off;
    }}
}}
# server {{
#     listen 443 ssl;
#     listen [::]:443 ssl;
#     server_name {domain_name};
#     ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
#     ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';
#     location / {{
#         proxy_pass http://localhost:3000;
#         proxy_http_version 1.1;
#         proxy_set_header Upgrade $http_upgrade;
#         proxy_set_header Connection 'upgrade';
#         proxy_set_header Host $host;
#         proxy_cache_bypass $http_upgrade;
#         proxy_buffering off;
#     }}
# }}
    """

    sites_available_path = f"/etc/nginx/sites-available/{domain_name}"
    if os.path.exists(sites_available_path):
        if not get_user_response(f"Nginx configuration for domain {domain_name} already exists. Do you want to overwrite it? (y/n): "):
            print("Aborted Nginx configuration.")
            return

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        temp_path = f.name
        f.write(nginx_config)

    os.system(f"sudo mv {temp_path} {sites_available_path}")
    os.system(f"sudo chown root:root {sites_available_path}")
    os.system(f"sudo chmod 644 {sites_available_path}")
    os.system(f"sudo ln -sf /etc/nginx/sites-available/{domain_name} /etc/nginx/sites-enabled/")
    is_successful, _, error = safe_system_call("sudo nginx -t")
    if not is_successful:
        print("Error: Nginx configuration test failed.")
        print(error)
        return

    if get_user_response("The Nginx configuration was verified. Do you want to restart Nginx? (y/n): "):
        is_successful, _, _ = safe_system_call("sudo systemctl restart nginx")

        if is_successful:
            print("Nginx restarted with the new configuration.")
        else:
            print("Job for nginx.service failed because the control process exited with error code.")
            _, status_output, _ = safe_system_call("systemctl status nginx.service")
            print("Output of 'systemctl status nginx.service':")
            print(status_output)
            _, journal_output, _ = safe_system_call("journalctl -xe")
            print("Output of 'journalctl -xe':")
            print(journal_output)

    else:
        print("Nginx was not restarted. Apply the new configuration by restarting Nginx manually.")

    if is_certbot_installed():
        print("Certbot is installed. Do you want to set up SSL with Certbot? (y/n): ")
        if get_user_response("Do you want to set up SSL with Certbot? (y/n): "):
            step3_setup_ssl_certbot()
        else:
            print("SSL setup with Certbot skipped.")

def is_certbot_installed():
    try:
        subprocess.check_output("which certbot", shell=True)
        return True
    except subprocess.CalledProcessError:
        return False

def is_nginx_running():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(("localhost", 80))
            return True
    except (socket.timeout, socket.error) as e:
        return False

def verify_domain_accessible(domain):
    try:
        response = requests.get(f"http://{domain}")
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def step3_setup_ssl_certbot(bottom_win):
    global domain_name

    load_domain_name_from_file()

    if not domain_name:
        print("Domain name is not set. Please configure Nginx first.")
        return

    if not is_nginx_running():
        print("Nginx is not running. Please start Nginx before setting up SSL.")
        return

    if not verify_domain_accessible(domain_name):
        print("The domain is not accessible from the public. Please check your Nginx configuration before setting up SSL.")
        return

    print("Setting up SSL with Certbot...")

    if not is_certbot_installed():
        if get_user_response("Certbot is not installed. Do you want to install it? (y/n): "):
            print("Installing Certbot...")
            os.system("sudo apt-get install -y certbot python3-certbot-nginx")
        else:
            print("Please install Certbot before setting up SSL.")
            return

    # Check if the certificate files exist
    cert_path = f"/etc/letsencrypt/live/{domain_name}/fullchain.pem"
    if not os.path.exists(cert_path):
        print(f"Certificate file not found at {cert_path}. Requesting a new SSL certificate for the domain...")
        os.system(f"sudo certbot --nginx -d {domain_name}")
    else:
        print("Certificate files already exist. Skipping certificate request.")

    # Check if Nginx configuration is valid
    config_test_result = subprocess.run(["sudo", "nginx", "-t"], capture_output=True, text=True)
    if config_test_result.returncode != 0:
        print("Nginx configuration test failed. Please fix the issues before proceeding.")
        print(config_test_result.stderr)
        return
    else:
        print("Nginx configuration test passed.")

    if get_user_response("Do you want to automatically renew SSL certificates? (y/n): "):
        print("Setting up automatic certificate renewal...")
        os.system('echo "0 5 * * * /usr/bin/certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null')
    else:
        print("Automatic certificate renewal not set up.")

    print("SSL setup with Certbot completed.")

def step4_install_docker_docker_compose_git(bottom_win):
    print(colored("Installing Docker, Docker Compose, and Git...", "cyan"))

    print(colored("Installing Git...", "cyan"))
    os.system("sudo apt-get install -y git")

    print(colored("Installing Docker...", "cyan"))
    os.system("sudo apt-get install -y docker.io")
    os.system("sudo systemctl enable --now docker")

    print(colored("Installing Docker Compose...", "cyan"))
    os.system("sudo apt-get install -y docker-compose")

    current_user = getpass.getuser()
    if current_user == "root":
        print(colored("\nWarning: It's not recommended to run Docker as root.", "yellow"))
        print(colored("Please choose a different user to add to the docker group:", "yellow"))

        home_users = [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d))]
        
        if len(home_users) == 1 and "root" in home_users:
            if get_user_response(colored("No users found other than root. Do you want to create a new user? (y/n): ", "yellow")):
                new_user = create_new_user()
                home_users.append(new_user)
            else:
                print(colored("Aborted adding a user to the docker group.", "red"))
                return

        for idx, user in enumerate(home_users):
            print(colored(f"{idx + 1}. {user}", "green"))

        while True:
            selected_user = input(colored("\nEnter the number of the user you want to add to the docker group: ", "yellow"))
            try:
                selected_user = int(selected_user)
                if 1 <= selected_user <= len(home_users):
                    break
                else:
                    print(colored("Invalid selection. Please try again.", "red"))
            except ValueError:
                print(colored("Invalid input. Please enter a number.", "red"))

        selected_user = home_users[selected_user - 1]
        if selected_user == "root":
            if not get_user_response(colored("Are you sure you want to add root to the docker group? (y/n): ", "yellow")):
                print(colored("Aborted adding root to the docker group.", "red"))
                return
    else:
        selected_user = current_user

    print(colored(f"Adding {selected_user} to the docker group...", "cyan"))
    os.system(f"sudo usermod -aG docker {selected_user}")

    print(colored("Installation of Docker, Docker Compose, and Git completed.", "green"))
    print("Installing Docker, Docker Compose, and Git...")

    print("Installing Git...")
    os.system("sudo apt-get install -y git")

    print("Installing Docker...")
    os.system("sudo apt-get install -y docker.io")
    os.system("sudo systemctl enable --now docker")

    print("Installing Docker Compose...")
    os.system("sudo apt-get install -y docker-compose")

    current_user = getpass.getuser()
    if current_user == "root":
        print("\nWarning: It's not recommended to run Docker as root.")
        print("Please choose a different user to add to the docker group:")

        home_users = [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d))]
        
        if len(home_users) == 1 and "root" in home_users:
            if get_user_response("No users found other than root. Do you want to create a new user? (y/n): "):
                new_user = create_new_user()
                home_users.append(new_user)
            else:
                print("Aborted adding a user to the docker group.")
                return

        for idx, user in enumerate(home_users):
            print(f"{idx + 1}. {user}")

        while True:
            selected_user = input("\nEnter the number of the user you want to add to the docker group: ")
            try:
                selected_user = int(selected_user)
                if 1 <= selected_user <= len(home_users):
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        selected_user = home_users[selected_user - 1]
        if selected_user == "root":
            if not get_user_response("Are you sure you want to add root to the docker group? (y/n): "):
                print("Aborted adding root to the docker group.")
                return
    else:
        selected_user = current_user

    print(f"Adding {selected_user} to the docker group...")
    os.system(f"sudo usermod -aG docker {selected_user}")

    print("Installation of Docker, Docker Compose, and Git completed.")

def check_docker_group_membership():
    user = getpass.getuser()
    group_members = grp.getgrnam("docker").gr_mem
    return user in group_members

def add_user_to_docker_group():
    user = getpass.getuser()
    os.system(f"sudo usermod -aG docker {user}")
    print(f"{user} has been added to the 'docker' group. Please log out and log back in for the changes to take effect.")

def step5_setup_gpt_chatbot_ui(bottom_win):
    print("Setting up GPT Chatbot UI...")

    # Step 1: Change to the appropriate directory
    if getpass.getuser() == "root":
        os.chdir("/opt")
    else:
        os.chdir(os.path.expanduser("~"))

    # Step 2: Download the GitHub repo
    os.system("git clone https://github.com/mckaywrigley/chatbot-ui.git")

    # Step 3: Change into the chatbot-ui directory
    os.chdir("chatbot-ui")

    # Step 4: Rename .env.local.example to .env.local
    if os.path.exists(".env.local.example"):
        shutil.move(".env.local.example", ".env.local")
    else:
        print("Warning: .env.local.example file not found. Skipping this step. Please ensure the .env.local file is properly configured.")

    # Step 5: Ask the user for input based on the following VARS
    env_vars = {
        "OPENAI_API_KEY": "",
        "OPENAI_API_HOST": "https://api.openai.com",
        "OPENAI_API_TYPE": "openai",
        "OPENAI_API_VERSION": "2023-03-15-preview",
        "AZURE_DEPLOYMENT_ID": "",
        "OPENAI_ORGANIZATION": "",
        "DEFAULT_MODEL": "gpt-3.5-turbo",
        "NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT": "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
        "GOOGLE_API_KEY": "",
        "GOOGLE_CSE_ID": ""
    }

    while True:
        for key, default_value in env_vars.items():
            user_input = input(f"Enter {key} (default: '{default_value}'): ")
            env_vars[key] = user_input.strip() or default_value

        print("\nPlease verify the entered values:")
        for key, value in env_vars.items():
            print(f"{key}: {value}")

        user_input = input("\nIs the information correct? (y/n): ")
        if user_input.lower() == "y":
            break

        # Check if the .env.local file exists
        if os.path.exists(".env.local"):
            if not get_user_response("The .env.local file already exists. Do you want to overwrite it? (y/n): "):
                print("Skipping overwriting the .env.local file.")
            else:
                # Save and overwrite the vars in the .env.local file
                with open(".env.local", "w") as f:
                    for key, value in env_vars.items():
                        f.write(f"{key}={value}\n")
        else:
            # Create and write the vars in the .env.local file
            with open(".env.local", "w") as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")

    # Test the docker-compose
    print("Testing the docker-compose...")
    test_result = os.system("docker-compose config")
    if test_result != 0:
        print("There are errors in the docker-compose configuration. Please fix them before proceeding.")
        return

    # Check if the user is part of the Docker group
    if not check_docker_group_membership():
        print("You need to be a member of the 'docker' group to start the services.")
        user_input = input("Do you want to be added to the 'docker' group? (y/n): ")
        if user_input.lower() == "y":
            add_user_to_docker_group()
            print("Please log out and log back in, and then run the script again to start the services.")
            return
        else:
            print("You will need to add yourself to the 'docker' group manually to start the services.")

    # Ask the user if they wish to start the services
    user_input = input("Do you want to start the services? (y/n): ")
    if user_input.lower() == "y":
        os.system("docker-compose up -d")
        print("Services started.")
    else:
        print("To start the services manually, run 'docker-compose up -d' in the chatbot-ui directory.")
        print("To stop the services, run 'docker-compose down' in the chatbot-ui directory.")

    print("GPT Chatbot UI setup completed.")

def update_gpt_chatbot_ui():
    print("Checking for updates in GPT Chatbot UI...")

    # Step 1: Change back to the user directory
    os.chdir(os.path.expanduser("~"))

    # Step 2: Check if the chatbot-ui directory exists
    if not os.path.exists("chatbot-ui"):
        print("GPT Chatbot UI is not installed. Please run the setup_gpt_chatbot_ui() function first.")
        return

    os.chdir("chatbot-ui")

    # Step 3: Fetch updates from the remote repository
    os.system("git fetch")

    # Step 4: Check if there are updates available
    updates_available = os.system("git diff --quiet origin/main")
    if updates_available != 0:
        print("Updates are available.")
        if get_user_response("Do you want to update GPT Chatbot UI? (y/n): "):
            # Step 5: Pull updates from the remote repository
            os.system("git pull")

            # Step 6: Shut down the old Docker image
            print("Shutting down the old Docker image...")
            os.system("docker-compose down")

            # Step 7: Create a new Docker image based on the updated docker-compose.yml file
            print("Creating a new Docker image...")
            os.system("docker-compose up -d")

            print("GPT Chatbot UI update completed.")
        else:
            print("Update canceled.")
    else:
        print("GPT Chatbot UI is already up to date.")

def download_file(url, local_path):
    response = requests.get(url)
    with open(local_path, "wb") as f:
        f.write(response.content)

def add_nimdys_login_form():
    print("Adding Nimdys login form...")

    add_login_form = get_user_response("Do you want to add Nimdys login form? (y/n): ")
    if not add_login_form:
        print("Aborted adding Nimdys login form.")
        return

    # Check if the chatbot-ui directory exists in the user's home directory or /opt/
    chatbot_ui_path = None
    user_home_dir = os.path.expanduser("~")
    possible_paths = [os.path.join(user_home_dir, "chatbot-ui"), "/opt/chatbot-ui"]

    for path in possible_paths:
        if os.path.exists(path):
            chatbot_ui_path = path
            break

    if chatbot_ui_path is None:
        print("GPT Chatbot UI is not installed. Please run the setup_gpt_chatbot_ui() function first.")
        return

    # Download and add LoginForm.tsx to chatbot-ui/Settings/
    shutil.copy(os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx"),
                os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx.bak"))
    download_file("https://github.com/Nimdy/chatgpt-menu-installer/raw/main/plugins/LoginForm.tsx",
                  os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx"))

    # Download and replace _app.tsx in chatbot-ui/pages/
    shutil.copy(os.path.join(chatbot_ui_path, "pages/_app.tsx"),
                os.path.join(chatbot_ui_path, "pages/_app.tsx.bak"))
    download_file("https://github.com/Nimdy/chatgpt-menu-installer/raw/main/plugins/_app.tsx",
                  os.path.join(chatbot_ui_path, "pages/_app.tsx"))

    # Execute the commands in addlibs.txt
    response = requests.get("https://github.com/Nimdy/chatgpt-menu-installer/raw/main/plugins/addlibs.txt")
    commands = response.text.splitlines()
    for command in commands:
        os.system(command)

    # Take input for each var or accept defaults
    env_vars = {
        "NEXT_PUBLIC_USERNAME": "UserName",
        "NEXT_PUBLIC_PASSWORD": "Password",
        "NEXT_PUBLIC_BYPASS_LOGIN": "True"
    }

    while True:
        for key, default_value in env_vars.items():
            user_input = input(f"Enter {key} (default: '{default_value}'): ")
            env_vars[key] = user_input.strip() or default_value

        print("\nPlease verify the entered values:")
        for key, value in env_vars.items():
            print(f"{key}: {value}")

        correct_info = get_user_response("\nIs the information correct? (y/n): ")
        if correct_info:
            break

    # Save and overwrite the vars in the .env.local file
    with open(os.path.join(chatbot_ui_path, ".env.local"), "a") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    # Check if .env.production file exists, create it if not, and add the vars
    env_production_file = os.path.join(chatbot_ui_path, ".env.production")
    if not os.path.exists(env_production_file):
        with open(env_production_file, "w") as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

    print("Nimdys login form added.")

def remove_nimdys_login_form():
    print("Removing Nimdys login form...")

    remove_login_form = get_user_response("Do you want to remove Nimdys login form? (y/n): ")
    if not remove_login_form:
        print("Aborted removing Nimdys login form.")
        return

    # Check if the chatbot-ui directory exists in the user's home directory or /opt/
    chatbot_ui_path = None
    user_home_dir = os.path.expanduser("~")
    possible_paths = [os.path.join(user_home_dir, "chatbot-ui"), "/opt/chatbot-ui"]

    for path in possible_paths:
        if os.path.exists(path):
            chatbot_ui_path = path
            break

    if chatbot_ui_path is None:
        print("GPT Chatbot UI is not installed. Please run the setup_gpt_chatbot_ui() function first.")
        return

    # Restore LoginForm.tsx in chatbot-ui/Settings/ if the backup exists
    login_form_backup = os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx.bak")
    if os.path.exists(login_form_backup):
        shutil.move(login_form_backup, os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx"))
    else:
        print("Warning: LoginForm.tsx backup not found. Skipping restoration.")

    # Restore _app.tsx in chatbot-ui/pages/ if the backup exists
    app_tsx_backup = os.path.join(chatbot_ui_path, "pages/_app.tsx.bak")
    if os.path.exists(app_tsx_backup):
        shutil.move(app_tsx_backup, os.path.join(chatbot_ui_path, "pages/_app.tsx"))
    else:
        print("Warning: _app.tsx backup not found. Skipping restoration.")

    print("Nimdys login form removed.")

def get_nginx_status():
    try:
        result = subprocess.run(['systemctl', 'is-active', 'nginx'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.stdout.strip() == 'active':
            return 'Running'
        else:
            return 'Stopped'
    except Exception as e:
        print(f"Error checking Nginx status: {e}")
        return 'Unknown'

def get_docker_status():
    try:
        container_name = 'chatbot-ui_chatgpt'
        result = subprocess.run(['docker', 'ps', '-a', '--filter', f'name={container_name}', '--format', '{{.Status}}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        status = result.stdout.strip()

        if status:
            return status
        else:
            return 'Not Found'
    except Exception as e:
        print(f"Error checking Docker status: {e}")
        return 'Unknown'
    
def get_domain_name():
    try:
        return socket.getfqdn()
    except Exception as e:
        print(f"Error retrieving domain name: {e}")
        return 'Unknown'

def get_ips():
    try:
        public_ip = requests.get("https://api.ipify.org").text
        return  public_ip
    except Exception as e:
        print(f"Error retrieving IP addresses: {e}")
        return 'Unknown', 'Unknown'

def get_total_connections():
    try:
        log_file_path = "/var/log/nginx/access.log"  # Update the path to the desired log file
        count = 0
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as f:
                for line in f:
                    count += 1
        return count
    except Exception as e:
        print(f"Error retrieving connection count: {e}")
        return 0

def get_active_connections():
    try:
        log_file_path = "/var/log/nginx/access.log"  # Update the path to the desired log file
        time_threshold = 300  # In seconds (e.g., 300 seconds equals 5 minutes)
        current_time = time.time()
        count = 0

        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as f:
                for line in f:
                    timestamp = re.search(r'\[(.*?)\]', line)
                    if timestamp:
                        log_time = time.mktime(time.strptime(timestamp.group(1), "%d/%b/%Y:%H:%M:%S %z"))
                        if (current_time - log_time) <= time_threshold:
                            count += 1

        return count
    except Exception as e:
        print(f"Error retrieving active connection count: {e}")
        return 0
    
def check_dependency_status():
    dependencies = {
        "git": "git --version",
        "docker": "docker --version",
        "docker-compose": "docker-compose --version",
        "nginx": "nginx -v",
        "certbot": "certbot --version",
        "chatbot-ui": os.path.expanduser("~") + "/chatbot-ui",
    }
    
    print("Checking dependencies...\n")

    for dependency, command in dependencies.items():
        print(f"Checking {dependency}... ", end="")

        if dependency == "chatbot-ui":
            status = os.path.exists(command)
        else:
            try:
                subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
                status = True
            except subprocess.CalledProcessError:
                status = False

        if status:
            print("\033[92m✔\033[0m")  # Green checkmark
        else:
            print("\033[91m✘\033[0m")  # Red cross

    print("\nDependency check completed.")

def print_dashboard(nginx_status, docker_status, domain_name, public_ip, total_connections, active_connections):
    print(colored("\n┌─────────────────────────────────────────────────────────────┐", "cyan"))
    print(colored(f"│          Chatbot UI Management Dashboard                    │", "cyan"))
    print(colored("├─────────────────────────────────────────────────────────────┤", "cyan"))
    print(colored(f"│  1. Nginx Server: {nginx_status}", "magenta"))
    print(colored(f"│  2. Docker Service Status: {docker_status}", "magenta"))
    print(colored(f"│  3. Domain Name: {domain_name}", "magenta"))
    print(colored(f"│  4. Public IP: {public_ip}", "magenta"))
    print(colored(f"│  5. Total UI Accesses: {total_connections}", "magenta"))
    print(colored(f"│  6. Active UI Accesses: {active_connections}", "magenta"))
    print(colored("└─────────────────────────────────────────────────────────────┘", "cyan"))

def print_menu():
    print(colored("\nMenu:", "green"))
    print(colored("1. Update & Upgrade System", "green"))
    print(colored("2. Install Chatbot UI by McKay Wrigley", "green"))
    print(colored("3. Add Nimdys Login Form", "green"))
    print(colored("4. Remove Nimdys Login Form", "green"))
    print(colored("5. Quick dependency check", "green"))
    print(colored("42. Check for updates - GPT Chatbot UI", "green"))
    print(colored("0. Exit", "green"))

def main():
    load_domain_name_from_file()
    while True:
        # Replace the placeholders with the relevant variables or function calls 
        nginx_status = get_nginx_status()    
        docker_status = get_docker_status()
        domain_name = get_domain_name()
        public_ip = get_ips()
        total_connections = get_total_connections()
        active_connections = get_active_connections()

        print_dashboard(nginx_status, docker_status, domain_name, public_ip, total_connections, active_connections)

        # Menu
        print_menu()

        choice = input(colored("\nEnter your choice: ", "yellow"))

        if choice == "1":
            step1_update_and_upgrade_system()
        elif choice == "2":
            main_installation_function()
        elif choice == "3":
            add_nimdys_login_form()
        elif choice == "4":
            remove_nimdys_login_form()
        elif choice == "5":
            check_dependency_status()   
        elif choice == "42":
            update_gpt_chatbot_ui()
        elif choice == "0":
            print(colored("Exiting... Close the Terminal to exit the script.", "red"))
            break
        else:
            print(colored("Invalid choice, please try again.", "red"))
if __name__ == "__main__":
    main()