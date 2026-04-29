FROM node:22-alpine

WORKDIR /app

# Instalamos dependencias primero (capa cacheada)
COPY package.json .
RUN npm install

# Copiamos el resto del código
COPY . .

# Vite dev server en el puerto 5173
CMD ["npm", "run", "dev"]
