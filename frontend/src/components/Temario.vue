<template>
  <div class="temario">
    <div v-for="modulo in modulos" :key="modulo.id" class="modulo">
      <h3 class="modulo-titulo">
        <span class="modulo-icon">ðŸ“š</span>
        {{ modulo.titulo }}
      </h3>
      <ul class="clases-lista">
        <li
          v-for="clase in modulo.clases"
          :key="clase.id"
          class="clase-item"
          :class="{ gratis: clase.es_gratis }"
        >
          <span class="clase-icon">
            <template v-if="clase.tipo_archivo === 'video'">ðŸŽ¬</template>
            <template v-else-if="clase.tipo_archivo === 'pdf'">ðŸ“„</template>
            <template v-else>ðŸ“</template>
          </span>
          <div class="clase-info">
            <span class="clase-titulo">{{ clase.titulo }}</span>
            <span class="clase-meta">
              {{ clase.tipo_archivo === "video" ? "Video" : "Apunte PDF" }}
              <template v-if="clase.duracion_minutos">
                Â· {{ clase.duracion_minutos }} min
              </template>
            </span>
          </div>
          <span v-if="clase.es_gratis" class="badge-gratis">Gratis</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
// Recibe los mÃ³dulos y clases del curso y los pinta en forma de temario
defineProps({ modulos: { type: Array, default: () => [] } });
</script>

<style scoped src="@/styles/Temario.css"></style>
