import axios from "axios";

// In dev mode, requests to /api are proxied by Vite to Django (see vite.config.ts).
// In production, change baseURL to your backend server's address.
export const apiClient = axios.create({
  baseURL: "/api/",
  headers: {
    "Content-Type": "application/json",
  },
});
