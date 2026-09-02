import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "../services/api";

export const useAuthStore = defineStore("auth", () => {
  const usuario = ref(JSON.parse(localStorage.getItem("usuario") || "null"));
  const token = ref(localStorage.getItem("token") || null);
  const refreshToken = ref(localStorage.getItem("refresh_token") || null);

  const isLoggedIn = computed(() => !!token.value);
  const esCreador = computed(
    () => usuario.value?.rol === "creador" || usuario.value?.rol === "administrador"
  );
  const esAdmin = computed(() => usuario.value?.rol === "administrador");

  function _guardar(usuarioData, tokenData, refreshTokenData) {
    token.value = tokenData;
    refreshToken.value = refreshTokenData;
    usuario.value = usuarioData;
    // localStorage guarda la sesión para que no se pierda al recargar la página
    localStorage.setItem("token", tokenData);
    localStorage.setItem("refresh_token", refreshTokenData);
    localStorage.setItem("usuario", JSON.stringify(usuarioData));
  }

  async function login(email, password) {
    // Pide el login al backend y guarda los tokens que devuelve
    const { data } = await api.post("/auth/login", { email, password });
    _guardar(data.usuario, data.token, data.refresh_token);
    return data;
  }

  async function register(datos) {
    const { data } = await api.post("/auth/register", datos);
    return data;
  }

  function logout() {
    token.value = null;
    refreshToken.value = null;
    usuario.value = null;
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("usuario");
  }

  async function refrescar() {
    // Usa el refresh token para conseguir un access token nuevo
    const { data } = await api.post(
      "/auth/refresh",
      {},
      { headers: { Authorization: `Bearer ${refreshToken.value}` } }
    );
    token.value = data.token;
    localStorage.setItem("token", data.token);
    return data.token;
  }

  return {
    usuario,
    token,
    refreshToken,
    isLoggedIn,
    esCreador,
    esAdmin,
    login,
    register,
    logout,
    refrescar,
  };
});
