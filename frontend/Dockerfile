FROM node:22.13.0

WORKDIR /app

COPY . .

RUN npm install --force

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]