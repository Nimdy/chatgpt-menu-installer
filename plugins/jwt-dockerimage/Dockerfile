# Start with the official Node.js image
FROM node:18

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy the rest of the application
COPY . .

# Set the environment variable for JWT secret (Replace 'your-jwt-secret' with your actual JWT secret)
ENV NEXT_PUBLIC_JWT_SECRET=your-jwt-secret

# Expose the port that your app will run on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]
