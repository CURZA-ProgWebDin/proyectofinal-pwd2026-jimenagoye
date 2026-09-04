<template>
  <div class="admin-curso">
    <h2 class="admin-titulo">Administrar curso</h2>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="mensajeOk" class="ok">{{ mensajeOk }}</p>

    <details class="admin-card">
      <summary>Editar datos del curso</summary>
      <form @submit.prevent="guardarCurso" class="curso-form">
        <div class="field">
          <label>Título</label>
          <input v-model="formCurso.titulo" type="text" required />
        </div>
        <div class="field">
          <label>Descripción</label>
          <textarea v-model="formCurso.descripcion" rows="3" required></textarea>
        </div>
        <div class="field-row">
          <div class="field">
            <label>Nivel</label>
            <select v-model="formCurso.nivel">
              <option value="">General</option>
              <option value="principiante">Principiante</option>
              <option value="intermedio">Intermedio</option>
              <option value="avanzado">Avanzado</option>
            </select>
          </div>
          <div class="field">
            <label>Año</label>
            <select v-model="formCurso.anio">
              <option :value="null">—</option>
              <option :value="1">Primer año</option>
              <option :value="2">Segundo año</option>
              <option :value="3">Tercer año</option>
            </select>
          </div>
          <div class="field">
            <label>Categoría</label>
            <input v-model="formCurso.categoria" type="text" />
          </div>
          <div class="field">
            <label>Precio ($)</label>
            <input v-model.number="formCurso.precio" type="number" min="0" step="0.01" />
          </div>
        </div>
        <div class="field">
          <label>URL de imagen</label>
          <input v-model="formCurso.imagen_url" type="url" />
        </div>
        <div class="field checkbox">
          <label>
            <input v-model="formCurso.activo" type="checkbox" />
            Curso activo (visible en el catálogo)
          </label>
        </div>
        <div class="acciones">
          <button type="submit" class="btn-primary" :disabled="cargando">
            Guardar cambios
          </button>
          <button type="button" class="btn-danger" @click="eliminarCurso">
            Eliminar curso
          </button>
        </div>
      </form>
    </details>

    <details class="admin-card">
      <summary>Agregar módulo</summary>
      <form @submit.prevent="agregarModulo" class="inline-form">
        <input v-model="nuevoModulo" type="text" placeholder="Título del módulo (ej: Unidad 1)" required />
        <button type="submit" class="btn-primary" :disabled="cargando">Agregar</button>
      </form>
    </details>

    <div v-if="!curso.modulos?.length" class="empty">
      Todavía no hay módulos. Agrega el primero con la opción de arriba.
    </div>

    <div v-for="modulo in curso.modulos" :key="modulo.id" class="modulo-admin">
      <div class="modulo-admin-head">
        <template v-if="editandoModuloId === modulo.id">
          <input v-model="tituloModuloEdit" type="text" class="edit-input" />
          <button class="btn-min" @click="guardarModulo(modulo)">✓</button>
          <button class="btn-min btn-ghost" @click="cancelarEdicionModulo">✕</button>
        </template>
        <template v-else>
          <h3 class="modulo-titulo">📚 {{ modulo.titulo }}</h3>
          <div class="modulo-acciones">
            <button class="btn-min" @click="iniciarEdicionModulo(modulo)">Editar</button>
            <button class="btn-min btn-ghost" @click="eliminarModulo(modulo)">Eliminar</button>
          </div>
        </template>
      </div>

      <ul class="clases-admin" v-if="modulo.clases?.length">
        <li v-for="clase in modulo.clases" :key="clase.id" class="clase-admin-item">
          <template v-if="editandoClaseId === clase.id">
            <div class="clase-edit">
              <input v-model="formClaseEdit.titulo" type="text" class="edit-input" placeholder="Título" />
              <input v-model.number="formClaseEdit.duracion_minutos" type="number" min="0" class="edit-input small" placeholder="Min" />
              <select v-model="formClaseEdit.tipo_archivo" class="edit-input small">
                <option value="video">Video</option>
                <option value="pdf">PDF</option>
              </select>
              <label class="chk">
                <input v-model="formClaseEdit.es_gratis" type="checkbox" /> Gratis
              </label>
              <button class="btn-min" @click="guardarClase(clase, modulo)">✓</button>
              <button class="btn-min btn-ghost" @click="editandoClaseId = null">✕</button>
            </div>
          </template>
          <template v-else>
            <div class="clase-fila">
              <span class="clase-icono">{{ iconoClase(clase.tipo_archivo) }}</span>
              <div class="clase-info">
                <strong>{{ clase.titulo }}</strong>
                <span class="clase-meta">
                  {{ clase.tipo_archivo === "video" ? "Video" : "PDF" }}
                  <template v-if="clase.duracion_minutos"> · {{ clase.duracion_minutos }} min</template>
                  <span v-if="clase.es_gratis" class="gratis"> · Gratis</span>
                </span>
              </div>
              <button class="btn-min" @click="iniciarEdicionClase(clase)">Editar</button>
              <button class="btn-min btn-ghost" @click="eliminarClase(clase, modulo)">Eliminar</button>
            </div>
          </template>
        </li>
      </ul>
      <p v-else class="empty-clases">Sin clases todavía.</p>

      <button class="btn-chico" @click="toggleFormClase(modulo.id)">
        {{ mostrarFormClase === modulo.id ? "Cerrar" : "+ Agregar clase" }}
      </button>

      <form v-if="mostrarFormClase === modulo.id" @submit.prevent="agregarClase" class="clase-form">
        <input v-model="formNuevaClase.titulo" type="text" placeholder="Título de la clase" required />
        <input v-model="formNuevaClase.url_archivo" type="url" placeholder="https://..." />
        <select v-model="formNuevaClase.tipo_archivo">
          <option value="video">Video</option>
          <option value="pdf">PDF</option>
        </select>
        <input v-model.number="formNuevaClase.duracion_minutos" type="number" min="0" placeholder="Duración (min)" />
        <label class="chk">
          <input v-model="formNuevaClase.es_gratis" type="checkbox" /> Gratis
        </label>
        <button type="submit" class="btn-primary" :disabled="cargando">Guardar clase</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from "vue";
import api from "../services/api";

const props = defineProps({
  curso: { type: Object, required: true },
});
const emit = defineEmits(["refresh", "eliminado"]);

const cargando = ref(false);
const error = ref("");
const mensajeOk = ref("");

const formCurso = reactive({
  titulo: "",
  descripcion: "",
  nivel: "",
  anio: null,
  categoria: "",
  precio: 0,
  imagen_url: "",
  activo: true,
});

// Cuando cambia el curso que llega por props, se vuelcan sus datos al formulario
watch(
  () => props.curso,
  (curso) => {
    if (!curso) return;
    Object.assign(formCurso, {
      titulo: curso.titulo,
      descripcion: curso.descripcion,
      nivel: curso.nivel || "",
      anio: curso.anio ?? null,
      categoria: curso.categoria || "",
      precio: Number(curso.precio) || 0,
      imagen_url: curso.imagen_url || "",
      activo: curso.activo,
    });
  },
  { immediate: true }
);

const nuevoModulo = ref("");
const editandoModuloId = ref(null);
const tituloModuloEdit = ref("");
const editandoClaseId = ref(null);
const formClaseEdit = reactive({ titulo: "", duracion_minutos: null, tipo_archivo: "video", es_gratis: false });
const mostrarFormClase = ref(null);
const formNuevaClase = reactive({
  titulo: "",
  url_archivo: "",
  tipo_archivo: "video",
  duracion_minutos: null,
  es_gratis: false,
});

function iconoClase(tipo) {
  // Elige el emoji según el tipo de archivo de la clase
  if (tipo === "video") return "🎬";
  if (tipo === "pdf") return "📄";
  return "📝";
}

async function notificar(fn) {
  // Ejecuta una acción de la API mostrando el error si falla
  error.value = "";
  mensajeOk.value = "";
  try {
    await fn();
  } catch (e) {
    error.value = e.response?.data?.error || "Error al ejecutar la acción";
  }
}

async function guardarCurso() {
  await notificar(async () => {
    const { data } = await api.put(`/cursos/${props.curso.id}`, formCurso);
    mensajeOk.value = data.mensaje;
    emit("refresh");
  });
}

async function eliminarCurso() {
  if (!window.confirm("¿Seguro que querés eliminar este curso?")) return;
  await notificar(async () => {
    await api.delete(`/cursos/${props.curso.id}`);
    emit("eliminado");
  });
}

async function agregarModulo() {
  await notificar(async () => {
    await api.post(`/cursos/${props.curso.id}/modulos`, { titulo: nuevoModulo.value });
    nuevoModulo.value = "";
    emit("refresh");
  });
}

function iniciarEdicionModulo(modulo) {
  editandoModuloId.value = modulo.id;
  tituloModuloEdit.value = modulo.titulo;
}
function cancelarEdicionModulo() {
  editandoModuloId.value = null;
}
async function guardarModulo(modulo) {
  await notificar(async () => {
    await api.put(`/cursos/${props.curso.id}/modulos/${modulo.id}`, {
      titulo: tituloModuloEdit.value,
    });
    editandoModuloId.value = null;
    emit("refresh");
  });
}

async function eliminarModulo(modulo) {
  if (!window.confirm(`¿Eliminar el módulo "${modulo.titulo}" y todas sus clases?`)) return;
  await notificar(async () => {
    await api.delete(`/cursos/${props.curso.id}/modulos/${modulo.id}`);
    emit("refresh");
  });
}

function toggleFormClase(moduloId) {
  mostrarFormClase.value = mostrarFormClase.value === moduloId ? null : moduloId;
}

async function agregarClase() {
  await notificar(async () => {
    await api.post(
      `/cursos/${props.curso.id}/modulos/${mostrarFormClase.value}/clases`,
      formNuevaClase
    );
    Object.assign(formNuevaClase, { titulo: "", url_archivo: "", tipo_archivo: "video", duracion_minutos: null, es_gratis: false });
    mostrarFormClase.value = null;
    emit("refresh");
  });
}

function iniciarEdicionClase(clase) {
  editandoClaseId.value = clase.id;
  Object.assign(formClaseEdit, {
    titulo: clase.titulo,
    duracion_minutos: clase.duracion_minutos,
    tipo_archivo: clase.tipo_archivo,
    es_gratis: clase.es_gratis,
  });
}

async function guardarClase(clase, modulo) {
  await notificar(async () => {
    await api.put(
      `/cursos/${props.curso.id}/modulos/${modulo.id}/clases/${clase.id}`,
      formClaseEdit
    );
    editandoClaseId.value = null;
    emit("refresh");
  });
}

async function eliminarClase(clase, modulo) {
  if (!window.confirm(`¿Eliminar la clase "${clase.titulo}"?`)) return;
  await notificar(async () => {
    await api.delete(
      `/cursos/${props.curso.id}/modulos/${modulo.id}/clases/${clase.id}`
    );
    emit("refresh");
  });
}
</script>

<style scoped src="@/styles/AdminCurso.css"></style>