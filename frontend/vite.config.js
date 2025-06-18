import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import { resolve } from "path";

export default defineConfig({
  plugins: [react()],
  root: ".",
  publicDir: "public",
  server: {
    host: "0.0.0.0",
    port: 5000,
    proxy: {
      "/api": {
        target: "http://localhost:8000", // Match backend port
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
    watch: {
      usePolling: true,
    },
  },
  build: {
    outDir: "build",
    emptyOutDir: true,
    rollupOptions: {
      input: {
        main: resolve(__dirname, "public/index.html"),
      },
    },
    assetsDir: "assets",
    manifest: true,
  },
  resolve: {
    extensions: [".mjs", ".js", ".jsx", ".json", ".ts", ".tsx"],
    alias: {
      "@": resolve(__dirname, "./src"),
      "@components": resolve(__dirname, "./src/components"),
      "@assets": resolve(__dirname, "./public"),
    },
  },
  base: "/",
});
