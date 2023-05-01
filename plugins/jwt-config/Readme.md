# JWT Authentication Service for McKay Wrigley's Chatbot UI

This repository contains a Dockerfile and a simple Express app for handling JSON Web Token (JWT) authentication for the Chatbot UI using my LoginForm Plugin. The Dockerfile is used to build a Docker image, which simplifies deployment and allows for easy integration with the Chatbot UI Docker image.

## Why use a Dockerfile for JWT?

Using a Dockerfile to build a Docker image for the JWT authentication service provides several benefits:

1. Consistent environment: Docker ensures that the application runs in the same environment across different stages of development and deployment, reducing inconsistencies and errors.
2. Isolation: By running the authentication service in its own Docker container, it is isolated from other services, which improves security and maintainability.
3. Scalability: Docker containers can be easily scaled up or down to handle fluctuations in traffic, providing a more efficient use of resources.
4. Easy integration: By running the JWT authentication service and Chatbot UI in separate Docker containers, they can be easily integrated using Docker Compose or other container orchestration tools.

## index.js Overview

The `index.js` file is the main entry point for the Express app that handles JWT authentication. It listens for POST requests at `/api/authenticate` and expects a `username` and `password` in the body of the request. If the provided credentials match the expected username and password, the service generates a JWT token and sends it in the response. If the credentials do not match, it responds with a 403 status code.

## Configuration

To configure the JWT authentication service to work with the Chatbot UI Docker image, follow these steps:

1. Replace the `mockUsername` and `mockPassword` in the `index.js` file with the actual username and password, or implement your own logic to validate the provided credentials.
2. Replace the `your-jwt-secret` placeholder in the Dockerfile with your actual JWT secret. This secret will be used to sign and verify JWT tokens.
3. Build the JWT authentication service Docker image using the provided Dockerfile.
4. Ensure that the Chatbot UI Docker image is configured to send authentication requests to the JWT authentication service. This can be done by updating the API URL in the Chatbot UI code (utils/nimdy/jwtAuth.js)to point to the JWT authentication service (e.g., `http://localhost:3000/api/authenticate` if running on the same machine).

Once the JWT authentication service is running and the Chatbot UI is configured to send authentication requests to it, users will be required to provide valid credentials before accessing the Chatbot UI. The JWT token will be used to verify the user's authentication status in subsequent requests.
