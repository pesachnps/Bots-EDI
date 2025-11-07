import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  base: '/static/modern-edi/',  // Production base path for Django static files
  build: {
    outDir: 'dist',
    assetsDir: 'assets',
    emptyOutDir: true,
  },
  server: {
    port: 3000,
    proxy: {
      '/modern-edi/api': {
        target: 'http://localhost:8080',
        changeOrigin: true,
      }
    }
  }
})
