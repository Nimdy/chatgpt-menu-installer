#!/bin/bash

echo "Do you want to use Nimdy's login form? (y/n)"
read answer

if [ "$answer" == "y" ]; then
    echo "Adding LoginForm.tsx"
    curl -L -o "chatbot-ui/components/Settings/LoginForm.tsx" "https://raw.githubusercontent.com/Nimdy/chatgpt-menu-installer/main/plugins/LoginForm.tsx"

    echo "Replacing _app.tsx"
    curl -L -o "chatbot-ui/pages/_app.tsx" "https://raw.githubusercontent.com/Nimdy/chatgpt-menu-installer/main/plugins/_app.tsx"

    echo "Replacing or creating .env.local.example"
    curl -L -o "chatbot-ui/.env.local.example" "https://raw.githubusercontent.com/Nimdy/chatgpt-menu-installer/main/plugins/.env.local.example"

    echo "Installing additional libraries"
    curl -L -o "addlibs.txt" "https://raw.githubusercontent.com/Nimdy/chatgpt-menu-installer/main/plugins/addlibs.txt"
    while read lib; do
        npm install $lib
    done < addlibs.txt
    rm addlibs.txt

    echo "Enter NEXT_PUBLIC_USERNAME (default: UserName)"
    read username
    [ -z "$username" ] && username="UserName"

    echo "Enter NEXT_PUBLIC_PASSWORD (default: Password)"
    read password
    [ -z "$password" ] && password="Password"

    echo "Enter NEXT_PUBLIC_BYPASS_LOGIN (default: True)"
    read bypass_login
    [ -z "$bypass_login" ] && bypass_login="True"

    echo "NEXT_PUBLIC_USERNAME=$username" >> chatbot-ui/.env.local
    echo "NEXT_PUBLIC_PASSWORD=$password" >> chatbot-ui/.env.local
    echo "NEXT_PUBLIC_BYPASS_LOGIN=$bypass_login" >> chatbot-ui/.env.local

    echo "Setup complete."
else
    echo "Skipping Nimdy's login form setup."
fi
