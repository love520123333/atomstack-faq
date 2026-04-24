import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  // 本地开发用 '/'，GitHub Pages 部署时设置 VITE_BASE=/atomstack-faq/
  base: process.env.VITE_BASE || '/',
  server: {
    port: 5173,
    strictPort: true
  },
  build: {
    outDir: 'dist',
    assetsDir: 'assets'
  }
})
