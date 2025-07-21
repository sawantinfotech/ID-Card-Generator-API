import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',        // Allow external access
    port: 3000,
    strictPort: true,
    allowedHosts: [
      'all', // ✅ Allow all hosts — including Replit's dynamic domain
    ],
  },
});
