FROM node:latest
WORKDIR /usr/src/app
COPY ./au_bon_beurre_api/ /usr/src/app
RUN npm install
RUN npm ci --only=production
EXPOSE 8080
CMD [ "node", "index.js" ]