import { fileURLToPath, URL } from "node:url";
import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      // "@" apunta a la carpeta src para imports como "@/styles/Dashboard.css"
      "@": fileURLToPath(new URL("./src", import.meta.url)),
    },
  },
  server: {
    host: true,
    port: 5173,
    proxy: {
      "/api": {
        // En desarrollo, Vite reenvía las peticiones "/api" al backend y evita problemas de CORS
        target: process.env.VITE_PROXY_TARGET || "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
