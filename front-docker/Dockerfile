# Stage 1: Compile and Build angular codebase

# Use official node image as the base image
FROM node:latest as build

ENV FRONT_DOCKER_PORT 80

# Set the working directory
WORKDIR /usr/local/app

# Add the source code to app
COPY ./front-docker/front-repos/au_bon_beurre_front /usr/local/app/

# Copy the .env file so angular can know the API_EXTERNAL_PORT
COPY .env /usr/local/app/src/assets/config.env

# Install all the dependencies
# RUN npm install

# Generate the build of the application
RUN npm run build


# Stage 2: Serve app with nginx server

# Use official nginx image as the base image
FROM nginx:latest

# Copy the build output to replace the default nginx contents.
COPY --from=build /usr/local/app/dist/un_bon_beurre_front /usr/share/nginx/html

# Expose port 80
EXPOSE ${FRONT_DOCKER_PORT}