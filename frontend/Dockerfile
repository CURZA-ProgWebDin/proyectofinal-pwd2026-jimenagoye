FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./  # copia primero las dependencias para aprovechar la caché de Docker
RUN npm install

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5173"]  # --host 0.0.0.0: accesible desde fuera del contenedor
