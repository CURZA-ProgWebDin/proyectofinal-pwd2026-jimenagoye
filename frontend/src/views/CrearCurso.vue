<template>
  <div class="crear-curso">
    <h1>Crear Nuevo Curso</h1>
    <form @submit.prevent="handleCrear" class="curso-form">
      <div class="field">
        <label>Título del curso</label>
        <input v-model="form.titulo" type="text" required placeholder="Ej: Álgebra Lineal I" />
      </div>
      <div class="field">
        <label>Descripción</label>
        <textarea v-model="form.descripcion" rows="4" required placeholder="Describí de qué trata el curso..."></textarea>
      </div>
      <div class="field-row">
        <div class="field">
          <label>Año</label>
          <select v-model="form.anio">
            <option :value="1">Primer año</option>
            <option :value="2">Segundo año</option>
            <option :value="3">Tercer año</option>
          </select>
        </div>
        <div class="field">
          <label>Categoría</label>
          <input v-model="form.categoria" type="text" placeholder="Ej: Matemática" />
        </div>
        <div class="field">
          <label>Precio ($)</label>
          <input v-model.number="form.precio" type="number" min="0" step="0.01" />
        </div>
      </div>
      <div class="field">
        <label>URL de imagen de portada</label>
        <input v-model="form.imagen_url" type="url" placeholder="https://..." />
      </div>
      <p v-if="error" class="error">{{ error }}</p>
      <button type="submit" class="btn-primary btn-block" :disabled="cargando">
        {{ cargando ? "Creando..." : "Crear Curso" }}
      </button>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";

const router = useRouter();
const form = reactive({
  titulo: "",
  descripcion: "",
  anio: 1,
  categoria: "",
  precio: 0,
  imagen_url: "",
});
const error = ref("");
const cargando = ref(false);

async function handleCrear() {
  error.value = "";
  cargando.value = true;
  try {
    const { data } = await api.post("/cursos/", form);  // crea el curso en el backend
    router.push(`/cursos/${data.curso.id}`);  // y navega al detalle del curso recién creado
  } catch (e) {
    error.value = e.response?.data?.error || "Error al crear el curso";
  } finally {
    cargando.value = false;
  }
}
</script>

<style scoped src="@/styles/CrearCurso.css"></style>
