<template>
  <div class="catalogo">
    <div class="catalogo-header">
      <h1>Catálogo de Cursos</h1>
      <div class="filtros">
        <input
          v-model="busqueda"  <!-- Mantiene sincronizado el valor de la caja de texto con variable busqueda -->
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