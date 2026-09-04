<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Iniciar Sesión</h2>
      <form @submit.prevent="handleLogin">
        <div class="field">
          <label>Email</label>
          <input v-model="email" type="email" required placeholder="tu@email.com" />
        </div>
        <div class="field">
          <label>Contraseña</label>
          <input v-model="password" type="password" required placeholder="••••••••" />
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn-primary btn-block" :disabled="cargando">
          {{ cargando ? "Entrando..." : "Iniciar Sesión" }}
        </button>
      </form>
      <p class="auth-link">
        ¿No tenés cuenta?
        <router-link to="/registro">Registrate acá</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const email = ref("");
const password = ref("");
const error = ref("");
const cargando = ref(false);
const router = useRouter();
const auth = useAuthStore();

async function handleLogin() {
  error.value = "";
  cargando.value = true;
  try {
    await auth.login(email.value, password.value);  // autentica en el backend y guarda los tokens
    router.push("/dashboard");  // redirige al panel una vez logueado
  } catch (e) {
    error.value = e.response?.data?.error || "Error al iniciar sesión";
  } finally {
    cargando.value = false;
  }
}
</script>