# Start from the Node.js 20.10.0 Alpine base image
FROM node:20.10.0-alpine3.19

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json (or npm's package-lock.json)
COPY package*.json ./

# Install npm packages
RUN npm install

# Copy the rest of the application's source code
COPY . .

# Build the application
RUN npm run build

# Use the startup script as the entry point
ENTRYPOINT ["node", "build"]