#!/usr/bin/env python3
import os
import getpass
import subprocess
import requests
import shutil
import socket

domain_name = None

def save_domain_name_to_file():
    with open("domain_name.txt", "w") as f:
        f.write(domain_name)

def load_domain_name_from_file():
    global domain_name

    try:
        with open("domain_name.txt", "r") as f:
            domain_name = f.read().strip()
    except FileNotFoundError:
        print("Domain name not found. It will be set during the Nginx configuration process.")

def get_user_response(prompt):
    while True:
        response = input(prompt).strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def safe_system_call(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def update_and_upgrade_system():
    print("Updating the package list...")
    os.system("sudo apt-get update")

    print("Upgrading the system...")
    os.system("sudo apt-get upgrade -y")

    print("Cleaning up unused packages...")
    os.system("sudo apt-get autoremove -y")

    print("System update and upgrade completed.")
    print("Please reboot the system to apply the changes.")
    print("After rebooting, run this script again to continue with menu option 2.")

def create_new_user():
    while True:
        new_username = input("Enter a new username: ").strip()
        if not new_username:
            print("Username cannot be empty. Please try again.")
            continue

        exists = subprocess.run(f"getent passwd {new_username}", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0
        if exists:
            print("The provided username already exists. Please try another username.")
            continue
        else:
            break

    password = getpass.getpass(f"Enter the password for {new_username}: ")
    confirm_password = getpass.getpass(f"Confirm the password for {new_username}: ")

    while password != confirm_password:
        print("Passwords don't match. Please try again.")
        password = getpass.getpass(f"Enter the password for {new_username}: ")
        confirm_password = getpass.getpass(f"Confirm the password for {new_username}: ")

    encrypted_password = subprocess.check_output(f"openssl passwd -1 {password}", shell=True, text=True).strip()

    os.system(f"sudo useradd -m -p {encrypted_password} {new_username}")
    os.system(f"sudo usermod -aG sudo {new_username}")
    print(f"User {new_username} created with sudo permissions.")
    return new_username

def install_docker_docker_compose_git():
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

def check_nginx_running():
    try:
        output = subprocess.check_output("systemctl is-active nginx", shell=True)
        return output.strip().decode("utf-8") == "active"
    except subprocess.CalledProcessError:
        return False

def is_domain_publicly_visible(domain_name):
    try:
        ip_address = socket.gethostbyname(domain_name)
        return True, ip_address
    except socket.gaierror:
        return False, None

def configure_nginx():
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
        print(f"Warning: The domain name {domain_name} is not publicly visible in DNS. This might cause issues with Certbot.")
    else:
        print(f"The domain name {domain_name} is publicly visible and resolves to IP address {ip_address}.")

    if not domain_visible:
        if not get_user_response("Do you want to continue with the configuration? (y/n): "):
            print("Aborted Nginx configuration.")
            return
        
    if is_certbot_installed() and is_nginx_running() and verify_domain_accessible(domain_name):
        setup_ssl_certbot()
    else:
        print("Skipping SSL-related configuration due to missing requirements or some other error.")        
        
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
server {{
    listen 443 ssl;
    listen [::]:443 ssl;
    server_name {domain_name};
    ssl_certificate /etc/letsencrypt/live/{domain_name}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/{domain_name}/privkey.pem;
    ssl_protocols TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers 'TLS_AES_128_GCM_SHA256:TLS_AES_256_GCM_SHA384:TLS_CHACHA20_POLY1305_SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384';
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
    """
    sites_available_path = f"/etc/nginx/sites-available/{domain_name}"
    if os.path.exists(sites_available_path):
        if not get_user_response(f"Nginx configuration for domain {domain_name} already exists. Do you want to overwrite it? (y/n): "):
            print("Aborted Nginx configuration.")
            return

    with open(sites_available_path, "w") as f:
        f.write(nginx_config)

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


    if not domain_name:
        domain_name = input("Enter the domain name (e.g., gpt.domain.com) where your GPT bot will be hosted: ")
        save_domain_name_to_file()

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

def setup_ssl_certbot():
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


def setup_gpt_chatbot_ui():
    print("Setting up GPT Chatbot UI...")

    # Step 1: Change back to the user directory
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

    # Save and overwrite the vars in the .env.local file
    with open(".env.local", "w") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    # Test the docker-compose
    print("Testing the docker-compose...")
    test_result = os.system("docker-compose config")
    if test_result != 0:
        print("There are errors in the docker-compose configuration. Please fix them before proceeding.")
        return

    # Ask the user if they wish to start the services
    user_input = input("Do you want to start the services? (y/n): ")
    if user_input.lower() == "y":
        os.system("docker-compose up -d")
        print("Services started.")
    else:
        print("To start the services manually, run 'docker-compose up -d' in the chatbot-ui directory.")
        print("To stop the services, run 'docker-compose down' in the chatbot-ui directory.")

    print("GPT Chatbot UI setup completed.")

def download_file(url, local_path):
    response = requests.get(url)
    with open(local_path, "wb") as f:
        f.write(response.content)

def add_nimdys_login_form():
    print("Adding Nimdys login form...")

    user_input = input("Do you want to add Nimdys login form? (y/n): ")
    if user_input.lower() != "y":
        print("Aborted adding Nimdys login form.")
        return

    # Download and add LoginForm.tsx to chatbot-ui/Settings/
    shutil.copy("chatbot-ui/Settings/LoginForm.tsx", "chatbot-ui/Settings/LoginForm.tsx.bak")
    download_file("https://github.com/Nimdy/chatgpt-menu-installer/raw/main/plugins/LoginForm.tsx",
                  "chatbot-ui/Settings/LoginForm.tsx")

    # Download and replace _app.tsx in chatbot-ui/pages/
    shutil.copy("chatbot-ui/pages/_app.tsx", "chatbot-ui/pages/_app.tsx.bak")
    download_file("https://github.com/Nimdy/chatgpt-menu-installer/raw/main/plugins/_app.tsx",
                  "chatbot-ui/pages/_app.tsx")

    # Download and replace .env.local.example in chatbot-ui/
    shutil.copy("chatbot-ui/.env.local.example", "chatbot-ui/.env.local.example.bak")
    download_file("https://github.com/Nimdy/chatgpt-menu-installer/raw/main/plugins/.env.local.example",
                  "chatbot-ui/.env.local.example")

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

        user_input = input("\nIs the information correct? (y/n): ")
        if user_input.lower() == "y":
            break

    # Save and overwrite the vars in the .env.local file
    with open("chatbot-ui/.env.local", "a") as f:
        for key, value in env_vars.items():
            f.write(f"{key}={value}\n")

    print("Nimdys login form added.")

def remove_nimdys_login_form():
    print("Removing Nimdys login form...")

    user_input = input("Do you want to remove Nimdys login form? (y/n): ")
    if user_input.lower() != "y":
        print("Aborted removing Nimdys login form.")
        return

    # Restore LoginForm.tsx in chatbot-ui/Settings/
    shutil.move("chatbot-ui/Settings/LoginForm.tsx.bak", "chatbot-ui/Settings/LoginForm.tsx")

    # Restore _app.tsx in chatbot-ui/pages/
    shutil.move("chatbot-ui/pages/_app.tsx.bak", "chatbot-ui/pages/_app.tsx")

    print("Nimdys login form removed.")

def main():
    load_domain_name_from_file()
    while True:
        print("\nMenu:")
        print("1. Update & Upgrade System")
        print("2. Install Docker, Docker Compose, and Git, Configure Nginx, and Setup SSL with Certbot, and Setup GPT Chatbot UI")
        print("3. Add Nimdys Login Form")
        print("4. Remove Nimdys Login Form")
        print("0. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            update_and_upgrade_system()
        elif choice == "2":
            update_and_upgrade_system()
            install_docker_docker_compose_git()
            configure_nginx()
            setup_ssl_certbot()
            setup_gpt_chatbot_ui()
        elif choice == "3":
            add_nimdys_login_form()
        elif choice == "4":
            remove_nimdys_login_form()
        elif choice == "0":
            print("Exiting... Close the Terminal to exit the script.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()