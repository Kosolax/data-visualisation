FROM node:latest
ENV PORT_TO_EXPOSE 8080

WORKDIR /usr/src/app
COPY ./au_bon_beurre_api/ /usr/src/app
RUN npm install
RUN npm ci --only=production
EXPOSE ${PORT_TO_EXPOSE}
CMD [ "node", "index.js" ]