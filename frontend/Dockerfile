# Use official Node.js image
FROM node:16

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN yarn install

# Build the project
RUN yarn build

# Expose port
EXPOSE 3000

# Command to serve the application
CMD ["yarn", "start"]