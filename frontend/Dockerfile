FROM node:22.13.0

WORKDIR /app

COPY . .

RUN npm install

RUN npm build

EXPOSE 3000

CMD ["npm", "start"]