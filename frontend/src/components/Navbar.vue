<template>
  <nav class="navbar">
    <div class="navbar-inner">
      <router-link to="/" class="navbar-brand">
        <span class="brand-bubble">AcademiaPlus</span>
      </router-link>

      <div class="navbar-links">
        <router-link to="/cursos" class="nav-link">Catálogo</router-link>

        <!-- Enlace visibles solo si hay sesión iniciada -->
        <template v-if="auth.isLoggedIn">
          <router-link to="/dashboard" class="nav-link">Mi Perfil</router-link>
          <router-link v-if="auth.esCreador" to="/crear-curso" class="nav-link">
            Crear Curso
          </router-link>
          <router-link v-if="auth.esAdmin" to="/admin/usuarios" class="nav-link">
            Admin
          </router-link>
          <div class="nav-user">
            <span class="nav-rol">{{ auth.usuario.rol }}</span>
            <span class="nav-nombre">{{ auth.usuario.nombre }}</span>
            <button @click="handleLogout" class="btn-logout">Salir</button>
          </div>
        </template>

        <template v-else>
          <router-link to="/login" class="nav-link">Iniciar Sesión</router-link>
          <router-link to="/registro" class="btn-register">Registrarse</router-link>
        </template>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from "../stores/auth";
import { useRouter } from "vue-router";

const auth = useAuthStore();
const router = useRouter();

function handleLogout() {
  auth.logout(); // limpia tokens y usuario del localStorage
  router.push("/");
}
</script>

<style scoped src="@/styles/Navbar.css"></style>
