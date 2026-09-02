<template>
  <router-link :to="`/cursos/${curso.id}`" class="curso-card">
    <div
      class="card-imagen"
      :style="{ backgroundImage: `url(${curso.imagen_url || imagenDefault})` }"
    >
      <span class="card-nivel">{{ curso.nivel || "General" }}</span>
      <span class="card-precio" v-if="curso.precio > 0">
        ${{ curso.precio }}
      </span>
      <span class="card-precio gratis" v-else>Gratis</span>
    </div>
    <div class="card-body">
      <h3 class="card-titulo">{{ curso.titulo }}</h3>
      <p class="card-descripcion">{{ curso.descripcion }}</p>
      <div class="card-meta">
        <span class="card-creador">{{ curso.creador_nombre }}</span>
        <span class="card-inscripciones">
          {{ curso.total_inscripciones }} inscriptos
        </span>
      </div>
    </div>
  </router-link>
</template>

<script setup>
defineProps({ curso: { type: Object, required: true } });

// Imagen de respaldo por si el curso no tiene una propia
const imagenDefault =
  "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=600&q=80";
</script>

<style scoped src="@/styles/CursoCard.css"></style>
