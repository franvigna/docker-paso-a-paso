import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    // Escucha en todas las interfaces para ser accesible desde fuera del contenedor
    host: true,
    port: 5173,
  },
})
