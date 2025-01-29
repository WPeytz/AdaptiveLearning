# Force the build to use amd64 architecture
FROM --platform=linux/amd64 nginx:alpine

# Remove the default nginx config
RUN rm /etc/nginx/conf.d/default.conf

# Copy a new Nginx configuration
COPY nginx.conf /etc/nginx/conf.d

# Copy built frontend files
COPY dist /usr/share/nginx/html

# Expose Cloud Run's required port
EXPOSE 8080

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]