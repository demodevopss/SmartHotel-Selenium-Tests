# Use a lightweight Nginx image as the base
FROM nginx:alpine

# Copy the website files from the current directory to the Nginx web root
COPY . /usr/share/nginx/html

# Expose port 80 to allow traffic to the web server
EXPOSE 80

# The command to run when the container starts
CMD ["nginx", "-g", "daemon off;"]
