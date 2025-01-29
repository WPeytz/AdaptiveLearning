# Use Node.js as the base image
FROM --platform=linux/amd64 node:18-alpine as build

# Set working directory
WORKDIR /app

# Copy package.json and install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the project files
COPY . .

# Build the project
RUN npm run build

# Use Nginx to serve the frontend
FROM nginx:alpine

# Copy built frontend from previous stage
COPY --from=build /app/dist /usr/share/nginx/html

# Expose the port (Google Cloud Run dynamically assigns this)
EXPOSE 8080

# Allow Nginx to listen on the dynamic PORT
RUN sh -c "echo 'server { listen ${PORT:-8080}; server_name _; location / { root /usr/share/nginx/html; index index.html; } }' > /etc/nginx/conf.d/default.conf"

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]