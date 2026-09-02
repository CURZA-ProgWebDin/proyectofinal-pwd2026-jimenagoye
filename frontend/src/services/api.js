import axios from "axios";
import { useAuthStore } from "../stores/auth";
import router from "../routes";

// Instancia única de Axios: todas las peticiones salen con base "/api"
const api = axios.create({
  baseURL: "/api",
  headers: { "Content-Type": "application/json" },
});

function decodificarToken(token) {
  if (!token) return null;
  try {
    const payload = token.split(".")[1];
    const base64 = payload.replace(/-/g, "+").replace(/_/g, "/");
    const padded = base64.padEnd(
      base64.length + ((4 - (base64.length % 4)) % 4),
      "="
    );
    const json = decodeURIComponent(
      atob(padded)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(json);
  } catch {
    return null;
  }
}

let refreshEnCurso = null;

function ejecutarRefresh() {
  if (!refreshEnCurso) {
    const auth = useAuthStore();
    refreshEnCurso = auth
      .refrescar()
      .catch((err) => {
        auth.logout();
        router.push("/login");
        throw err;
      })
      .finally(() => {
        refreshEnCurso = null;
      });
  }
  return refreshEnCurso;
}

api.interceptors.request.use(async (config) => {
  const isRefresh = (config.url || "").includes("/auth/refresh");
  if (isRefresh) return config;

  const auth = useAuthStore();
  const payload = decodificarToken(auth.token);  // lee la fecha de expiración que viaja dentro del token

  // Renovación anticipada: si el access token expira en menos de 60s, se renueva antes de usarlo.
  if (auth.token && auth.refreshToken && payload?.exp) {
    const segundosRestantes = payload.exp - Date.now() / 1000;
    if (segundosRestantes < 60) {
      await ejecutarRefresh();
    }
  }

  if (auth.token) {
    config.headers.Authorization = `Bearer ${auth.token}`;  // adjunta el token al header de la petición
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const auth = useAuthStore();
    const original = error.config;
    const url = (original?.url || "").includes("/auth/refresh");

    // Access token expirado: se intenta renovar una vez y se reenvía la petición original.
    if (error.response?.status === 401 && original && !original._reintentado && auth.refreshToken && !url) {
      original._reintentado = true;
      try {
        await ejecutarRefresh();
        return api(original);
      } catch (e) {
        return Promise.reject(e);
      }
    }

    // Refresh inválido o sin token de refresco: se cierra la sesión.
    if (error.response?.status === 401 && original && !url) {
      auth.logout();
      router.push("/login");  // sin sesión válida, devuelve al usuario al formulario de login
    }

    return Promise.reject(error);
  }
);

export default api;