<template>
  <div class="home">
    <section class="hero">
      <div class="hero-content">
        <h1>EDG desde cero</h1>
        <p>Lleva la cursada al dÃ­a ðŸ©º</p>
        <router-link to="/cursos" class="hero-btn">Explorar Cursos</router-link>
      </div>
    </section>

    <section class="cursos-destacados">
      <h2 class="section-title">Ãšltimos cursos</h2>
      <div class="cursos-grid">
        <CursoCard
          v-for="curso in cursos"
          :key="curso.id"
          :curso="curso"
        />
      </div>
      <p v-if="cursos.length === 0" class="empty-state">
        AÃºn no hay cursos publicados.
      </p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import api from "../services/api";
import CursoCard from "../components/CursoCard.vue";

const cursos = ref([]);

onMounted(async () => {
  try {
    const { data } = await api.get("/cursos/?per_page=6");  // pide los Ãºltimos cursos a la API
    cursos.value = data.cursos;
  } catch (e) {
    console.error("Error al cargar cursos", e);
  }
});
</script>

<style scoped src="@/styles/Home.css"></style>
