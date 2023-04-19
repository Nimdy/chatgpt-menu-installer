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
import textwrap
import contextlib

from termcolor import colored

domain_name = None

def read_progress_file(progress_filename):
    if os.path.exists(progress_filename):
        with open(progress_filename, "r") as f:
            return int(f.read().strip())
    else:
        with open(progress_filename, "w") as f:
            f.write("0")
        return 0

def update_progress_file(progress_filename, step):
    with open(progress_filename, "w") as f:
        f.write(str(step))

def run_command_with_curses(command, bottom_win):
    print(f"Executing command: {command}")
    y, x = bottom_win.getyx()
    max_y, max_x = bottom_win.getmaxyx()
    bottom_win.scrollok(True)
    exit_code = None
    with os.popen(command) as stream:
        for line in stream:
            wrapped_lines = textwrap.wrap(line.strip(), max_x)
            for wrapped_line in wrapped_lines:
                if y >= max_y - 1:
                    bottom_win.scroll(1)
                    y -= 1
                bottom_win.addstr(y, 0, wrapped_line)
                y += 1
            bottom_win.refresh()
        exit_code = stream.close()
    bottom_win.scrollok(False)
    return exit_code

def add_wrapped_text(text, bottom_win):
    max_x = bottom_win.getmaxyx()[1]
    wrapped_lines = textwrap.wrap(text, max_x)
    for line in wrapped_lines:
        bottom_win.addstr(line + "\n")
    bottom_win.refresh()

def curses_context(stdscr):
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(True)
    try:
        yield
    finally:
        # Clean up curses
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()

def main_installation_function():
    progress_filename = "installation_progress.txt"
    
    if os.path.exists(progress_filename):
        saved_step = read_progress_file(progress_filename)
    else:
        saved_step = 0

    # Initialize curses
    stdscr = curses.initscr()

    with curses_context(stdscr):
        # Divide the screen into two parts
        top_win = curses.newwin(5, curses.COLS, 0, 0)
        bottom_win = curses.newwin(curses.LINES - 5, curses.COLS, 5, 0)
        load_domain_name_from_file(bottom_win)

        def update_step_status(step):
            top_win.clear()
            for i in range(1, step):
                top_win.addstr(1, 2 + (i - 1) * 15, f"[✓] Step {i}")
            top_win.addstr(1, 2 + (step - 1) * 15, f"[✗] Step {step}")
            top_win.refresh()

        for step in range(saved_step + 1, 6):
            update_step_status(step)
            if step == 1:
                step1_update_and_upgrade_system(bottom_win)
            elif step == 2:
                step2_configure_nginx(bottom_win)
            elif step == 3:
                step3_setup_ssl_certbot(bottom_win)
            elif step == 4:
                step4_install_docker_docker_compose_git(bottom_win)
            elif step == 5:
                step5_setup_gpt_chatbot_ui(bottom_win)
            update_progress_file(progress_filename, step)

    # Remove the progress file once the installation is complete
    if os.path.exists(progress_filename):
        os.remove(progress_filename)

def save_domain_name_to_file(domain_name, bottom_win):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    domain_name_file = os.path.join(script_dir, "domain_name.txt")
    
    with open(domain_name_file, "w") as f:
        f.write(domain_name)
    
    bottom_win.addstr(f"Domain name saved to {domain_name_file}\n")
    bottom_win.refresh()

def load_domain_name_from_file(bottom_win=None):
    try:
        with open("domain_name.txt", "r") as f:
            domain_name = f.read().strip()
    except FileNotFoundError:
        domain_name = ""
        if bottom_win:
            bottom_win.addstr("Domain name not found. It will be set during the Nginx configuration process.\n")
            bottom_win.refresh()
    
    return domain_name

def get_user_response(prompt, bottom_win=None):
    bottom_win.addstr(prompt)
    bottom_win.refresh()
    curses.echo()

    while True:
        response = bottom_win.getstr().strip().decode("utf-8").lower()

        if response in ['y', 'n']:
            y, x = bottom_win.getyx()
            max_y, max_x = bottom_win.getmaxyx()
            if y == max_y - 1:
                bottom_win.move(y, 0)
            else:
                bottom_win.addstr("\n")
            bottom_win.refresh()
            curses.noecho()
            return response == 'y'
        else:
            bottom_win.addstr("Invalid input. Please enter 'y' or 'n'.\n")
            bottom_win.refresh()

def safe_system_call(cmd):
    if isinstance(cmd, str):
        cmd = cmd.split()
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.returncode == 0, result.stdout, result.stderr

def step1_update_and_upgrade_system(bottom_win):
    add_wrapped_text("Updating the package list...", bottom_win)
    run_command_with_curses("sudo apt-get update", bottom_win)

    add_wrapped_text("Upgrading the system...", bottom_win)
    run_command_with_curses("sudo apt-get upgrade -y", bottom_win)

    add_wrapped_text("Cleaning up unused packages...", bottom_win)
    run_command_with_curses("sudo apt-get autoremove -y", bottom_win)

    add_wrapped_text("System update and upgrade completed.", bottom_win)
    add_wrapped_text("Please reboot the system to apply the changes.", bottom_win)
    add_wrapped_text("After rebooting, run this script again to continue with menu option 2.", bottom_win)

def create_new_user(bottom_win):
    while True:
        bottom_win.addstr("Enter a new username: ")
        bottom_win.refresh()
        curses.echo()  # Enable echo
        new_username = bottom_win.getstr().decode("utf-8").strip()
        curses.noecho()  # Disable echo

        if not new_username:
            bottom_win.addstr("Username cannot be empty. Please try again.\n")
            bottom_win.refresh()
            continue

        exists, _, _ = safe_system_call(f"getent passwd {new_username}")
        if exists:
            bottom_win.addstr("The provided username already exists. Please try another username.\n")
            bottom_win.refresh()
            continue
        else:
            break

    bottom_win.addstr(f"Enter the password for {new_username}: ")
    bottom_win.refresh()
    password = bottom_win.getstr().decode("utf-8")
    
    bottom_win.addstr(f"Confirm the password for {new_username}: ")
    bottom_win.refresh()
    confirm_password = bottom_win.getstr().decode("utf-8")

    while password != confirm_password:
        bottom_win.addstr("Passwords don't match. Please try again.\n")
        bottom_win.refresh()
        bottom_win.addstr(f"Enter the password for {new_username}: ")
        bottom_win.refresh()
        password = bottom_win.getstr().decode("utf-8")
        bottom_win.addstr(f"Confirm the password for {new_username}: ")
        bottom_win.refresh()
        confirm_password = bottom_win.getstr().decode("utf-8")

    encrypted_password = subprocess.check_output(["openssl", "passwd", "-1", password], text=True).strip()

    safe_system_call(f"sudo useradd -m -p {encrypted_password} {new_username}")
    safe_system_call(f"sudo usermod -aG sudo {new_username}")
    bottom_win.addstr(f"User {new_username} created with sudo permissions.\n")
    bottom_win.refresh()
    return new_username

def check_nginx_running(bottom_win):
    success, output, _ = safe_system_call("systemctl is-active nginx")
    return success and output.strip() == "active"

def is_domain_publicly_visible(domain_name, bottom_win):
    try:
        domain_ip = socket.gethostbyname(domain_name)
    except socket.gaierror as e:
        bottom_win.addstr(f"Error resolving domain: {e}\n")
        bottom_win.refresh()
        return False

    try:
        public_ip = requests.get("https://api64.ipify.org").text
    except requests.RequestException as e:
        bottom_win.addstr(f"Error getting public IP: {e}\n")
        bottom_win.refresh()
        return False

    if domain_ip == public_ip:
        return True
    else:
        bottom_win.addstr(f"Domain IP ({domain_ip}) does not match public IP ({public_ip}).\n")
        bottom_win.refresh()
        return False

def step2_configure_nginx(bottom_win):
    global domain_name
    add_wrapped_text("Configuring Nginx...", bottom_win)

    if not check_nginx_running(bottom_win):
        if get_user_response("Nginx is not running. Do you want to install and start Nginx? (y/n): ", bottom_win):
            add_wrapped_text("Installing Nginx...", bottom_win)
            run_command_with_curses("sudo apt-get install -y nginx", bottom_win)
            add_wrapped_text("Starting Nginx...", bottom_win)
            run_command_with_curses("sudo systemctl start nginx", bottom_win)
        else:
            add_wrapped_text("Please install and start Nginx before configuring.", bottom_win)
            return

    if not get_user_response("Do you want to add a new domain to the Nginx configuration? (y/n): ", bottom_win):
        add_wrapped_text("Aborted Nginx configuration.", bottom_win)
        return

    bottom_win.addstr("Enter the domain name (e.g., gpt.domain.com) where your GPT bot will be hosted: ")
    bottom_win.refresh()
    curses.echo()  # Enable echo
    domain_name = bottom_win.getstr().strip().decode("utf-8")
    curses.noecho()  # Disable echo
    bottom_win.addstr("\n")
    bottom_win.refresh()
    bottom_win.clrtobot()  # Clear the screen from the current cursor position to the bottom

    if not is_domain_publicly_visible(domain_name, bottom_win):
        add_wrapped_text(f"Warning: The domain name {domain_name} either does not resolve in the global DNS or does not resolve to the public IP address. This might cause issues with Certbot.", bottom_win)
    else:
        add_wrapped_text(f"The domain name {domain_name} is publicly visible.", bottom_win)
        save_domain_name_to_file(domain_name, bottom_win)

    if not is_domain_publicly_visible(domain_name, bottom_win):
        if not get_user_response("Do you want to continue with the configuration? (y/n): ", bottom_win):
            add_wrapped_text("Aborted Nginx configuration.", bottom_win)
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
        if not get_user_response(f"Nginx configuration for domain {domain_name} already exists. Do you want to overwrite it? (y/n): ", bottom_win):
            bottom_win.addstr("Aborted Nginx configuration.\n")
            bottom_win.refresh()
            return

    with tempfile.NamedTemporaryFile("w", delete=False) as f:
        temp_path = f.name
        f.write(nginx_config)

    run_command_with_curses(f"sudo mv {temp_path} {sites_available_path}", bottom_win)
    run_command_with_curses(f"sudo chown root:root {sites_available_path}", bottom_win)
    run_command_with_curses(f"sudo chmod 644 {sites_available_path}", bottom_win)
    run_command_with_curses(f"sudo ln -sf /etc/nginx/sites-available/{domain_name} /etc/nginx/sites-enabled/", bottom_win)
    is_successful, _, error = safe_system_call("sudo nginx -t")
    if not is_successful:
        bottom_win.addstr("Error: Nginx configuration test failed.\n")
        bottom_win.addstr(error + "\n")
        bottom_win.refresh()     
        print(error)
        return

    if get_user_response("The Nginx configuration was verified. Do you want to restart Nginx? (y/n): ", bottom_win):
        is_successful, _, _ = safe_system_call("sudo systemctl restart nginx")

        if is_successful:
            bottom_win.addstr("Nginx restarted with the new configuration.\n")
            bottom_win.refresh()
        else:
            bottom_win.addstr("Job for nginx.service failed because the control process exited with error code.\n")
            bottom_win.refresh()
            _, status_output, _ = safe_system_call("systemctl status nginx.service")
            bottom_win.addstr("Output of 'systemctl status nginx.service':\n")
            bottom_win.addstr(status_output + "\n")
            bottom_win.refresh()
            _, journal_output, _ = safe_system_call("journalctl -xe")
            bottom_win.addstr("Output of 'journalctl -xe':\n")
            bottom_win.addstr(journal_output + "\n")
            bottom_win.refresh()

    else:
        bottom_win.addstr("Nginx was not restarted. Apply the new configuration by restarting Nginx manually.\n")
        bottom_win.refresh()

    if is_certbot_installed(bottom_win):
        if get_user_response("Certbot is installed. Do you want to set up SSL with Certbot? (y/n): ", bottom_win):
            step3_setup_ssl_certbot(bottom_win)
        else:
            bottom_win.addstr("SSL setup with Certbot skipped.\n")
            bottom_win.refresh()
    else:
        if get_user_response("Certbot is not installed. Do you want to install Certbot and set up SSL? (y/n): ", bottom_win):
            bottom_win.addstr("Installing Certbot...\n")
            bottom_win.refresh()
            run_command_with_curses("sudo apt-get install -y certbot python3-certbot-nginx", bottom_win)
            step3_setup_ssl_certbot(bottom_win)
        else:
            bottom_win.addstr("Certbot installation and SSL setup skipped.\n")
            bottom_win.refresh()

def is_certbot_installed(bottom_win):
    success, _, _ = safe_system_call("which certbot")
    return success

def is_nginx_running():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect(("localhost", 80))
            return True
    except (socket.timeout, socket.error) as e:
        return False

def step3_setup_ssl_certbot(bottom_win):
    global domain_name

    if not is_domain_publicly_visible(domain_name, bottom_win):
        bottom_win.addstr("The domain is not accessible from the public. Please check your Nginx configuration before setting up SSL.\n")
        bottom_win.refresh()
        return

    bottom_win.addstr("Setting up SSL with Certbot...\n")
    bottom_win.refresh()

    # Check if the certificate files exist
    cert_path = f"/etc/letsencrypt/live/{domain_name}/fullchain.pem"
    if not os.path.exists(cert_path):
        add_wrapped_text(f"Certificate file not found at {cert_path}. Requesting a new SSL certificate for the domain...", bottom_win)
        run_command_with_curses(f"sudo certbot --nginx -d {domain_name}", bottom_win)
    else:
        bottom_win.addstr("Certificate files already exist. Skipping certificate request.\n")
        bottom_win.refresh()

    # Check if Nginx configuration is valid
    config_test_result = subprocess.run(["sudo", "nginx", "-t"], capture_output=True, text=True)
    if config_test_result.returncode != 0:
        bottom_win.addstr("Nginx configuration test failed. Please fix the issues before proceeding.\n")
        bottom_win.addstr(config_test_result.stderr + "\n")
        bottom_win.refresh()
        return
    else:
        bottom_win.addstr("Nginx configuration test passed. With CertBot SSL Certs applied.\n")
        bottom_win.refresh()

    if get_user_response("Do you want to automatically renew SSL certificates? (y/n): ", bottom_win):
        bottom_win.addstr("Setting up automatic certificate renewal...\n")
        bottom_win.refresh()
        run_command_with_curses('echo "0 5 * * * /usr/bin/certbot renew --quiet" | sudo tee -a /etc/crontab > /dev/null', bottom_win)
    else:
        bottom_win.addstr("Automatic certificate renewal not set up.\n")
        bottom_win.refresh()

    bottom_win.addstr("SSL setup with Certbot completed.\n")
    bottom_win.refresh()

def step4_install_docker_docker_compose_git(bottom_win):
    add_wrapped_text("Installing Docker, Docker Compose, and Git...\n", bottom_win)

    add_wrapped_text("Installing Git...\n", bottom_win)
    run_command_with_curses("sudo apt-get install -y git", bottom_win)

    add_wrapped_text("Installing Docker...\n", bottom_win)
    run_command_with_curses("sudo apt-get install -y docker.io", bottom_win)
    run_command_with_curses("sudo systemctl enable --now docker", bottom_win)

    add_wrapped_text("Installing Docker Compose...\n", bottom_win)
    run_command_with_curses("sudo apt-get install -y docker-compose", bottom_win)

    current_user = getpass.getuser()
    if current_user == "root":
        add_wrapped_text("\nWarning: It's not recommended to run Docker as root.\nPlease choose a different user to add to the docker group:\n", bottom_win)

        home_users = [d for d in os.listdir('/home') if os.path.isdir(os.path.join('/home', d))]

        if len(home_users) == 1 and "root" in home_users:
            if get_user_response("No users found other than root. Do you want to create a new user? (y/n): ", bottom_win):
                new_user = create_new_user(bottom_win)
                home_users.append(new_user)
            else:
                add_wrapped_text("Aborted adding a user to the docker group.\n", bottom_win)
                return

        for idx, user in enumerate(home_users):
            add_wrapped_text(f"{idx + 1}. {user}", bottom_win)

        while True:
            selected_user = get_user_response("\nEnter the number of the user you want to add to the docker group: ", bottom_win)
            try:
                selected_user = int(selected_user)
                if 1 <= selected_user <= len(home_users):
                    break
                else:
                    add_wrapped_text("Invalid selection. Please try again.", bottom_win)
            except ValueError:
                add_wrapped_text("Invalid input. Please enter a number.", bottom_win)

        selected_user = home_users[selected_user - 1]
        if selected_user == "root":
            if not get_user_response("Are you sure you want to add root to the docker group? (y/n): ", bottom_win):
                add_wrapped_text("Aborted adding root to the docker group.", bottom_win)
                return
    else:
        selected_user = current_user

    add_wrapped_text(f"Adding {selected_user} to the docker group...", bottom_win)
    run_command_with_curses(f"sudo usermod -aG docker {selected_user}", bottom_win)

    # Restart Docker service
    run_command_with_curses("sudo systemctl restart docker", bottom_win)

    add_wrapped_text("Installation of Docker, Docker Compose, and Git completed.", bottom_win)

def check_docker_group_membership():
    user = getpass.getuser()
    group_members = grp.getgrnam("docker").gr_mem
    return user in group_members

def add_user_to_docker_group(bottom_win):
    user = getpass.getuser()
    bottom_win.addstr(f"Adding {user} to the docker group...\n")
    bottom_win.refresh()
    run_command_with_curses(f"sudo usermod -aG docker {user}", bottom_win)
    bottom_win.addstr("User added to the docker group. Please log out and log back in for the changes to take effect.\n")
    bottom_win.refresh()

def step5_setup_gpt_chatbot_ui(bottom_win):
    add_wrapped_text("Setting up GPT Chatbot UI...\n", bottom_win)

    # Step 1: Change to the appropriate directory
    if getpass.getuser() == "root":
        os.chdir("/opt")
    else:
        os.chdir(os.path.expanduser("~"))

    # Step 2: Download the GitHub repo
    run_command_with_curses("git clone https://github.com/mckaywrigley/chatbot-ui.git", bottom_win)

    # Step 3: Change into the chatbot-ui directory
    os.chdir("chatbot-ui")

    # Step 4: Rename .env.local.example to .env.local
    if os.path.exists(".env.local.example"):
        shutil.move(".env.local.example", ".env.local")
    else:
        add_wrapped_text("Warning: .env.local.example file not found. Skipping this step. Please ensure the .env.local file is properly configured.\n", bottom_win)

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
            bottom_win.addstr(f"Enter {key} (default: '{default_value}'): ")
            bottom_win.refresh()
            curses.echo()
            user_input = bottom_win.getstr().decode("utf-8")
            curses.noecho()
            env_vars[key] = user_input.strip() or default_value

        bottom_win.addstr("\nPlease verify the entered values:\n")
        bottom_win.refresh()
        for key, value in env_vars.items():
            bottom_win.addstr(f"{key}: {value}\n")
            bottom_win.refresh()

        if get_user_response("\nIs the information correct? (y/n): ", bottom_win):
            break
        bottom_win.refresh()
        curses.echo()
        user_input = bottom_win.getstr().decode("utf-8").lower()
        curses.noecho()
        if user_input == "y":
            break

   # Check if the .env.local file exists
    if os.path.exists(".env.local"):
        if get_user_response("The .env.local file already exists. Do you want to overwrite it? (y/n): ", bottom_win):
            # Save and overwrite the vars in the .env.local file
            with open(".env.local", "w") as f:
                for key, value in env_vars.items():
                    f.write(f"{key}={value}\n")
        else:
            add_wrapped_text("Skipping overwriting the .env.local file.\n", bottom_win)
    else:
        # Create and write the vars in the .env.local file
        with open(".env.local", "w") as f:
            for key, value in env_vars.items():
                f.write(f"{key}={value}\n")

    # Test the docker-compose
    add_wrapped_text("Testing the docker-compose...\n", bottom_win)
    test_result = run_command_with_curses("docker-compose config", bottom_win)

    if test_result != 0:
        add_wrapped_text("There are errors in the docker-compose configuration. Please fix them before proceeding.\n", bottom_win)
        return

    # Check if the user is part of the Docker group
    if not check_docker_group_membership():
        add_wrapped_text("You need to be a member of the 'docker' group to start the services.\n", bottom_win)
        if get_user_response("Do you want to be added to the 'docker' group? (y/n): ", bottom_win):
            add_user_to_docker_group(bottom_win)
            add_wrapped_text("You might have to log out and log back in, and then run the script again to start the services.\n", bottom_win)
            return
        else:
            add_wrapped_text("You will need to add yourself to the 'docker' group manually to start the services.\n", bottom_win)

    # Ask the user if they wish to start the services
    if get_user_response("Do you want to start the services? (y/n): ", bottom_win):
        run_command_with_curses("docker-compose up -d", bottom_win)
        add_wrapped_text("Services started.\n", bottom_win)
    else:
        add_wrapped_text("To start the services manually, run 'docker-compose up -d' in the chatbot-ui directory.\n", bottom_win)
        add_wrapped_text("To stop the services, run 'docker-compose down' in the chatbot-ui directory.\n", bottom_win)

    add_wrapped_text("GPT Chatbot UI setup completed.\n", bottom_win)

def update_gpt_chatbot_ui(bottom_win):
    add_wrapped_text("Checking for updates in GPT Chatbot UI...\n", bottom_win)

    # Step 1: Change back to the user directory
    if getpass.getuser() == "root":
        os.chdir("/opt")
    else:
        os.chdir(os.path.expanduser("~"))

    # Step 2: Check if the chatbot-ui directory exists
    if not os.path.exists("chatbot-ui"):
        add_wrapped_text("GPT Chatbot UI is not installed. Please run the setup_gpt_chatbot_ui() function first.\n", bottom_win)
        return

    os.chdir("chatbot-ui")

    # Step 3: Fetch updates from the remote repository
    run_command_with_curses("git fetch", bottom_win)

    # Step 4: Check if there are updates available
    updates_available = os.system("git diff --quiet origin/main")
    if updates_available != 0:
        add_wrapped_text("Updates are available.\n", bottom_win)
        if get_user_response("Do you want to update GPT Chatbot UI? (y/n): ", bottom_win):
            # Step 5: Pull updates from the remote repository
            run_command_with_curses("git pull", bottom_win)

            # Step 6: Shut down the old Docker image
            add_wrapped_text("Shutting down the old Docker image...\n", bottom_win)
            run_command_with_curses("docker-compose down", bottom_win)

            # Step 7: Create a new Docker image based on the updated docker-compose.yml file
            add_wrapped_text("Creating a new Docker image...\n", bottom_win)
            run_command_with_curses("docker-compose up -d", bottom_win)

            add_wrapped_text("GPT Chatbot UI update completed.\n", bottom_win)
        else:
            add_wrapped_text("Update canceled.\n", bottom_win)
    else:
        add_wrapped_text("GPT Chatbot UI is already up to date.\n", bottom_win)

def download_file(url, local_path):
    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(local_path, "wb") as f:
            f.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")

def add_nimdys_login_form(bottom_win):
    bottom_win.addstr("Adding Nimdys login form...\n")
    bottom_win.refresh()

    add_login_form = get_user_response("Do you want to add Nimdys login form? (y/n): ", bottom_win)
    if not add_login_form:
        bottom_win.addstr("Aborted adding Nimdys login form.\n")
        bottom_win.refresh()
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
        bottom_win.addstr("GPT Chatbot UI is not installed. Please run the setup_gpt_chatbot_ui() function first.\n")
        bottom_win.refresh()
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
        success, stdout, stderr = safe_system_call(command)
        if not success:
            bottom_win.addstr(f"Error executing command: {command}\n{stderr}\n")
            bottom_win.refresh()

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

        bottom_win.addstr("\nPlease verify the entered values:\n")
        for key, value in env_vars.items():
            bottom_win.addstr(f"{key}: {value}\n")
        bottom_win.refresh()

        correct_info = get_user_response("\nIs the information correct? (y/n): ", bottom_win)
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

    bottom_win.addstr("Nimdys login form added.\n")
    bottom_win.refresh()

def remove_nimdys_login_form(bottom_win):
    bottom_win.addstr("Removing Nimdys login form...\n")
    bottom_win.refresh()

    remove_login_form = get_user_response("Do you want to remove Nimdys login form? (y/n): ", bottom_win)
    if not remove_login_form:
        bottom_win.addstr("Aborted removing Nimdys login form.\n")
        bottom_win.refresh()
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
        bottom_win.addstr("GPT Chatbot UI is not installed. Please run the setup_gpt_chatbot_ui() function first.\n")
        bottom_win.refresh()
        return

    # Restore LoginForm.tsx in chatbot-ui/Settings/ if the backup exists
    login_form_backup = os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx.bak")
    if os.path.exists(login_form_backup):
        shutil.move(login_form_backup, os.path.join(chatbot_ui_path, "Settings/LoginForm.tsx"))
    else:
        bottom_win.addstr("Warning: LoginForm.tsx backup not found. Skipping restoration.\n")
        bottom_win.refresh()

    # Restore _app.tsx in chatbot-ui/pages/ if the backup exists
    app_tsx_backup = os.path.join(chatbot_ui_path, "pages/_app.tsx.bak")
    if os.path.exists(app_tsx_backup):
        shutil.move(app_tsx_backup, os.path.join(chatbot_ui_path, "pages/_app.tsx"))
    else:
        bottom_win.addstr("Warning: _app.tsx backup not found. Skipping restoration.\n")
        bottom_win.refresh()

    bottom_win.addstr("Nimdys login form removed.\n")
    bottom_win.refresh()
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
    except FileNotFoundError:
        print("Docker command not found. Docker might not be installed.")
        return 'Docker not installed'
    except Exception as e:
        print(f"Error checking Docker status: {e}")
        return 'Error'
    
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
    def main_window(stdscr):
        curses.curs_set(0)  # Hide cursor
        stdscr.timeout(100)  # Refresh every 100 ms

        while True:
            stdscr.clear()

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

            choice = stdscr.getch()

            if choice == ord("1"):
                step1_update_and_upgrade_system()
            elif choice == ord("2"):
                main_installation_function()
            elif choice == ord("3"):
                add_nimdys_login_form()
            elif choice == ord("4"):
                remove_nimdys_login_form()
            elif choice == ord("5"):
                check_dependency_status()
            elif choice == ord("42"):
                update_gpt_chatbot_ui()
            elif choice == ord("0"):
                stdscr.addstr(colored("Exiting... Close the Terminal to exit the script.", "red"))
                stdscr.refresh()
                time.sleep(2)
                break
            elif choice != -1:
                stdscr.addstr(colored("Invalid choice, please try again.", "red"))
                stdscr.refresh()
                time.sleep(2)

    curses.wrapper(main_window)

if __name__ == "__main__":
    main()