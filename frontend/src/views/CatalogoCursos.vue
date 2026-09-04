<template>
  <div class="catalogo">
    <div class="catalogo-header">
      <h1 class="catalogo-titulo">Catálogo de Cursos</h1>
      <div class="filtros">
        <input
          v-model="busqueda"
          @input="buscarCursos"
          type="text"
          placeholder="Buscar cursos..."
          class="buscador"
        />
        <select v-model="anio" @change="buscarCursos" class="filtro-select">
          <option value="">Todos los años</option>
          <option value="1">Primer año</option>
          <option value="2">Segundo año</option>
          <option value="3">Tercer año</option>
        </select>
      </div>
    </div>
    <div class="cursos-grid">
      <CursoCard
        v-for="curso in cursos"
        :key="curso.id"
        :curso="curso"
      />
    </div>
    <p v-if="cursos.length === 0" class="empty-state">
      No se encontraron cursos con esos filtros.
    </p>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import CursoCard from "../components/CursoCard.vue";

const cursos = ref([]);
const busqueda = ref("");
const anio = ref("");

async function buscarCursos() {
  const params = { per_page: 24 };
  if (busqueda.value) params.q = busqueda.value;
  if (anio.value) params.anio = anio.value;
  const { data } = await api.get("/cursos/", { params });  // consulta el catálogo con los filtros elegidos
  cursos.value = data.cursos;
}

onMounted(buscarCursos);
</script>

<style scoped>
.catalogo {
  max-width: 1200px;
  margin: 0 auto;
  padding: 40px 24px 64px;
}

.catalogo-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  gap: 20px;
  margin-bottom: 36px;
}

.catalogo-titulo {
  font-size: 2rem;
  color: #111827;
  margin: 0;
  letter-spacing: -0.5px;
}

.filtros {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  align-items: center;
  gap: 12px;
  width: 100%;
  max-width: 640px;
}

.buscador,
.filtro-select {
  padding: 12px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 10px;
  font-size: 0.95rem;
  background: #fff;
  color: #111827;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.06);
  outline: none;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.buscador {
  flex: 1 1 260px;
  min-width: 200px;
}

.filtro-select {
  width: 190px;
  cursor: pointer;
}

.buscador:focus,
.filtro-select:focus {
  border-color: #111827;
  box-shadow: 0 0 0 3px rgba(17, 24, 39, 0.1);
}

.cursos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.cursos-grid :deep(.curso-card) {
  display: flex;
  flex-direction: column;
  background: #fffefb;
  border-radius: 16px;
  overflow: hidden;
  border: 1px solid #f0e9dc;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.cursos-grid :deep(.curso-card:hover) {
  transform: translateY(-6px);
  box-shadow: 0 14px 30px rgba(0, 0, 0, 0.12);
}

.cursos-grid :deep(.card-body) {
  flex: 1;
  padding: 18px;
}

.empty-state {
  color: #9ca3af;
  text-align: center;
  padding: 48px;
  font-size: 0.95rem;
}
</style>
