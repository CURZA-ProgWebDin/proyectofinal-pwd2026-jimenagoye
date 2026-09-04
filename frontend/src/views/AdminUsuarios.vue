<template>
  <div class="admin-usuarios">
    <div class="head">
      <h1>Administrar Usuarios</h1>
      <p class="subtitle">Total: {{ total }}</p>
    </div>

    <p v-if="error" class="error">{{ error }}</p>

    <table class="usuarios-table" v-if="usuarios.length">
      <thead>
        <tr>
          <th>ID</th>
          <th>Nombre</th>
          <th>Email</th>
          <th>Rol</th>
          <th>Fecha</th>
          <th>Estado</th>
          <th></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="usuario in usuarios" :key="usuario.id">
          <td>{{ usuario.id }}</td>
          <td>{{ usuario.nombre }}</td>
          <td>{{ usuario.email }}</td>
          <td>
            <span :class="['badge', usuario.rol]">{{ usuario.rol }}</span>
          </td>
          <td>{{ new Date(usuario.fecha_registro).toLocaleDateString() }}</td>
          <td>
            <span :class="['badge', usuario.activo ? 'activo' : 'inactivo']">
              {{ usuario.activo ? "Activo" : "Inactivo" }}
            </span>
          </td>
          <td>
            <button
              v-if="usuario.activo && usuario.id !== auth.usuario?.id"
              class="btn-desactivar"
              @click="desactivar(usuario)"
            >
              Desactivar
            </button>
          </td>
        </tr>
      </tbody>
    </table>
    <p v-else class="empty-state">No hay usuarios para mostrar.</p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import { useAuthStore } from "../stores/auth";

const auth = useAuthStore();
const usuarios = ref([]);
const total = ref(0);
const error = ref("");

async function cargarUsuarios() {
  try {
    const { data } = await api.get("/usuarios/?per_page=100"); // lista paginada de usuarios (admin)
    usuarios.value = data.usuarios;
    total.value = data.total;
  } catch (e) {
    error.value = e.response?.data?.error || "Error al cargar usuarios";
  }
}

async function desactivar(usuario) {
  if (!window.confirm(`¿Desactivar a ${usuario.nombre}?`)) return;
  try {
    await api.delete(`/usuarios/${usuario.id}`); // desactiva la cuenta del usuario
    await cargarUsuarios(); // recarga la tabla para reflejar el estado nuevo
  } catch (e) {
    error.value = e.response?.data?.error || "Error al desactivar";
  }
}

onMounted(cargarUsuarios);
</script>

<style scoped src="@/styles/AdminUsuarios.css"></style>