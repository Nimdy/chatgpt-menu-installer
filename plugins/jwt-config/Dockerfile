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

# Expose the port that your app will run on
EXPOSE 3000

# Start the application by running index.js
CMD ["node", "app/index.js"]