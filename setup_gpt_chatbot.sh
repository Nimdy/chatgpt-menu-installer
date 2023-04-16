#!/bin/bash

function install_dependencies() {
  sudo apt update
  sudo apt upgrade -y
  sudo apt install docker docker-compose git -y
  sudo systemctl enable docker.service
  sudo systemctl start docker.service
  sudo usermod -a -G docker $USER
}

function setup_docker_compose() {
  wget https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)
  sudo mv docker-compose-$(uname -s)-$(uname -m) /usr/local/bin/docker-compose
  sudo chmod -v +x /usr/local/bin/docker-compose
}

function clone_chatbot_ui() {
  git clone https://github.com/mckaywrigley/chatbot-ui.git
  cd chatbot-ui
}

function configure_chatbot_ui() {
  read -rp "Enter your OpenAI API Key: " openai_api_key
  read -rp "Enter your OpenAI API Host (default: https://api.openai.com): " openai_api_host
  read -rp "Enter your OpenAI API Type (default: openai): " openai_api_type
  read -rp "Enter your OpenAI API Version (default: 2023-03-15-preview): " openai_api_version
  read -rp "Enter your Azure Deployment ID (leave blank if not using Azure): " azure_deployment_id
  read -rp "Enter your OpenAI Organization (leave blank if not applicable): " openai_organization
  read -rp "Enter your Default Model (default: gpt-3.5-turbo): " default_model
  read -rp "Enter your Default System Prompt: " default_system_prompt
  read -rp "Enter your Google API Key: " google_api_key
  read -rp "Enter your Google CSE ID: " google_cse_id

  openai_api_host=${openai_api_host:-https://api.openai.com}
  openai_api_type=${openai_api_type:-openai}
  openai_api_version=${openai_api_version:-2023-03-15-preview}
  default_model=${default_model:-gpt-3.5-turbo}
  default_system_prompt=${default_system_prompt:-"You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown."}

  cat <<EOT > .env.local
OPENAI_API_KEY=$openai_api_key
OPENAI_API_HOST=$openai_api_host
OPENAI_API_TYPE=$openai_api_type
OPENAI_API_VERSION=$openai_api_version
AZURE_DEPLOYMENT_ID=$azure_deployment_id
OPENAI_ORGANIZATION=$openai_organization
DEFAULT_MODEL=$default_model
NEXT_PUBLIC_DEFAULT_SYSTEM_PROMPT=$default_system_prompt
GOOGLE_API_KEY=$google_api_key
GOOGLE_CSE_ID=$google_cse_id
EOT
}

function main() {
  echo "Installing dependencies..."
  install_dependencies

  echo "Setting up Docker Compose..."
  setup_docker_compose

  echo "Cloning Chatbot UI repository..."
  clone_chatbot_ui

  echo "Configuring Chatbot UI..."
  configure_chatbot_ui

  echo "GPT Chatbot setup complete."
}

main
