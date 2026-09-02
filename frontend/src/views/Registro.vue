<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2>Crear Cuenta</h2>
      <form @submit.prevent="handleRegister">
        <div class="field">
          <label>Nombre</label>
          <input v-model="form.nombre" type="text" required placeholder="Tu nombre" />
        </div>
        <div class="field">
          <label>Email</label>
          <input v-model="form.email" type="email" required placeholder="tu@email.com" />
        </div>
        <div class="field">
          <label>Contraseña</label>
          <input v-model="form.password" type="password" required placeholder="Mínimo 6 caracteres" />
        </div>
        <div class="field">
          <label>¿Qué querés hacer?</label>
          <select v-model="form.rol">
            <option value="alumno">Aprender (Alumno)</option>
            <option value="creador">Crear cursos (Creador)</option>
          </select>
        </div>
        <p v-if="error" class="error">{{ error }}</p>
        <button type="submit" class="btn-primary btn-block" :disabled="cargando">
          {{ cargando ? "Creando..." : "Registrarse" }}
        </button>
      </form>
      <p class="auth-link">
        ¿Ya tenés cuenta?
        <router-link to="/login">Iniciá sesión</router-link>
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const form = reactive({ nombre: "", email: "", password: "", rol: "alumno" });
const error = ref("");
const cargando = ref(false);
const router = useRouter();
const auth = useAuthStore();

async function handleRegister() {
  error.value = "";
  cargando.value = true;
  try {
    await auth.register(form);  // crea la cuenta nueva en el backend
    await auth.login(form.email, form.password);  // e inicia sesión automáticamente
    router.push("/dashboard");
  } catch (e) {
    error.value = e.response?.data?.error || "Error al registrarse";
  } finally {
    cargando.value = false;
  }
}
</script>

