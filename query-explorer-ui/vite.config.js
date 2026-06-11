import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/v1/statement': {
        target: 'http://localhost:8080',
        changeOrigin: true
      },
      '/minio': {
        target: 'http://localhost:9000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/minio/, '')
      },
      '/api/clickhouse': {
        target: 'http://localhost:8123',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/clickhouse/, '')
      }
    }
  }
})
