<template>
  <div class="detalle" v-if="curso">
    <div class="detalle-hero" :style="{ backgroundImage: `url(${curso.imagen_url || imagenDefault})` }">
      <div class="detalle-hero-overlay">
        <span class="nivel-badge">{{ curso.nivel }}</span>
        <h1>{{ curso.titulo }}</h1>
        <p>{{ curso.descripcion }}</p>
        <div class="detalle-meta">
          <span>Por {{ curso.creador_nombre }}</span>
          <span>{{ curso.total_inscripciones }} inscriptos</span>
          <span v-if="curso.precio > 0">${{ curso.precio }}</span>
          <span v-else class="gratis">Gratis</span>
        </div>
        <button
          v-if="auth.isLoggedIn && !inscrito"
          @click="inscribirse"
          class="btn-inscribirse"
        >
          Inscribirse
        </button>
        <span v-if="inscrito" class="inscrito-badge">Inscripto âœ“</span>
      </div>
    </div>
    <div class="detalle-body">
      <h2>Temario</h2>
      <Temario :modulos="curso.modulos || []" />
      <p v-if="!curso.modulos?.length" class="empty-temario">
        Este curso aÃºn no tiene mÃ³dulos cargados.
      </p>

      <AdminCurso
        v-if="puedeAdministrar"
        :curso="curso"
        @refresh="cargarCurso"
        @eliminado="irAlCatalogo"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import { useAuthStore } from "../stores/auth";
import Temario from "../components/Temario.vue";
import AdminCurso from "../components/AdminCurso.vue";

const route = useRoute();
const router = useRouter();
const auth = useAuthStore();
const curso = ref(null);
const inscrito = ref(false);

const puedeAdministrar = computed(
  () =>
    auth.esCreador &&
    curso.value &&
    (auth.esAdmin || curso.value.creador_id === auth.usuario?.id)
);

function irAlCatalogo() {
  router.push("/cursos");
}

const imagenDefault =
  "https://images.unsplash.com/photo-1516321318423-f06f85e504b3?w=1200&q=80";

async function cargarCurso() {
  const { data } = await api.get(`/cursos/${route.params.id}`);  // trae el detalle completo del curso
  curso.value = data;
}

async function inscribirse() {
  try {
    await api.post("/inscripciones/", { curso_id: curso.value.id });  // registra la inscripciÃ³n del alumno
    inscrito.value = true;
  } catch (e) {
    alert(e.response?.data?.error || "Error al inscribirse");
  }
}

onMounted(async () => {
  await cargarCurso();
  if (auth.isLoggedIn) {
    try {
      const { data } = await api.get("/inscripciones/");
      inscrito.value = data.some((i) => i.curso_id === curso.value.id && i.estado === "activa");
    } catch (e) { /* ignore */ }
  }
});
</script>

<style scoped src="@/styles/DetalleCurso.css"></style>
