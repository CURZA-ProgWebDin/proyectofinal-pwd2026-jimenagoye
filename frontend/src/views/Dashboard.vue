<template>
  <div class="dashboard">
    <div class="dashboard-header">
      <h1>Mi Perfil</h1>
      <p class="subtitle">Hola, {{ auth.usuario?.nombre }}</p>
    </div>

    <div class="tabs">
      <button
        v-for="tab in tabs"
        :key="tab.id"
        :class="['tab', { active: tabActual === tab.id }]"
        @click="tabActual = tab.id"
      >
        {{ tab.label }}
      </button>
    </div>

    <div class="tab-content">
      <div v-if="tabActual === 'cursos'" class="tab-panel">
        <div class="cursos-grid" v-if="misCursos.length">
          <CursoCard v-for="c in misCursos" :key="c.id" :curso="c" />
        </div>
        <p v-else class="empty-state">
          No estÃ¡s inscripto en ningÃºn curso.
          <router-link to="/cursos">Explorar cursos</router-link>
        </p>
      </div>

      <div v-if="tabActual === 'historial'" class="tab-panel">
        <table class="historial-table" v-if="inscripciones.length">
          <thead>
            <tr>
              <th>Curso</th>
              <th>Estado</th>
              <th>Progreso</th>
              <th>Fecha</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="insc in inscripciones" :key="insc.id">
              <td>{{ insc.curso_titulo }}</td>
              <td>
                <span :class="['badge', insc.estado]">{{ insc.estado }}</span>
              </td>
              <td>
                <div class="progress-bar">
                  <div class="progress-fill" :style="{ width: insc.progreso + '%' }"></div>
                </div>
                {{ insc.progreso }}%
              </td>
              <td>{{ new Date(insc.fecha_inscripcion).toLocaleDateString() }}</td>
              <td>
                <button
                  v-if="insc.estado === 'activa'"
                  class="btn-cancelar"
                  @click="cancelarInscripcion(insc)"
                >
                  Cancelar
                </button>
              </td>
            </tr>
          </tbody>
        </table>
        <p v-else class="empty-state">Sin inscripciones recientes.</p>
      </div>

      <div v-if="tabActual === 'perfil'" class="tab-panel perfil-panel">
        <div class="perfil-card">
          <div class="perfil-avatar">
            {{ auth.usuario?.nombre?.charAt(0)?.toUpperCase() }}
          </div>
          <div class="perfil-info">
            <h3>{{ auth.usuario?.nombre }}</h3>
            <p>{{ auth.usuario?.email }}</p>
            <span class="badge" :class="auth.usuario?.rol">{{ auth.usuario?.rol }}</span>
          </div>
        </div>
        <form @submit.prevent="guardarPerfil" class="perfil-form">
          <div class="field">
            <label>Nombre</label>
            <input v-model="perfilForm.nombre" type="text" />
          </div>
          <div class="field">
            <label>BiografÃ­a</label>
            <textarea v-model="perfilForm.biografia" rows="3"></textarea>
          </div>
          <button type="submit" class="btn-primary">Guardar Cambios</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from "vue";
import api from "../services/api";
import { useAuthStore } from "../stores/auth";
import CursoCard from "../components/CursoCard.vue";

const auth = useAuthStore();
const tabActual = ref("cursos");
const tabs = [
  { id: "cursos", label: "Mis Cursos" },
  { id: "historial", label: "Historial" },
  { id: "perfil", label: "Perfil" },
];

const misCursos = ref([]);
const inscripciones = ref([]);
const perfilForm = reactive({
  nombre: auth.usuario?.nombre || "",
  biografia: auth.usuario?.biografia || "",
});

onMounted(async () => {
  try {
    const [cursosRes, inscRes] = await Promise.all([
      api.get("/inscripciones/mis-cursos"),  // cursos en los que estÃ¡ inscripto el alumno
      api.get("/inscripciones/"),  // histÃ³rico de todas sus inscripciones
    ]);
    misCursos.value = cursosRes.data;
    inscripciones.value = inscRes.data;
  } catch (e) {
    console.error("Error al cargar dashboard", e);
  }
});

async function guardarPerfil() {
  try {
    const { data } = await api.put(`/usuarios/${auth.usuario.id}`, perfilForm);  // actualiza nombre y biografÃ­a del perfil
    auth.usuario = data.usuario;
    localStorage.setItem("usuario", JSON.stringify(data.usuario));
    alert("Perfil actualizado");
  } catch (e) {
    alert("Error al guardar");
  }
}

async function cancelarInscripcion(insc) {
  if (!window.confirm(`Â¿Cancelar la inscripciÃ³n a "${insc.curso_titulo}"?`)) return;
  try {
    await api.delete(`/inscripciones/${insc.id}`);  // cancela la inscripciÃ³n (mÃ©todo DELETE)
    const [cursosRes, inscRes] = await Promise.all([
      api.get("/inscripciones/mis-cursos"),
      api.get("/inscripciones/"),
    ]);
    misCursos.value = cursosRes.data;
    inscripciones.value = inscRes.data;
  } catch (e) {
    alert(e.response?.data?.error || "Error al cancelar inscripciÃ³n");
  }
}
</script>

<style scoped src="@/styles/Dashboard.css"></style>
