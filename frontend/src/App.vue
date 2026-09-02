<template>
  <div id="app">
    <Navbar /> <!-- barra común a todas las vistas -->
    <main class="main-content">
      <router-view /> <!-- aquí renderiza la vista activa según la ruta -->
    </main>
  </div>
</template>

<script setup>
import Navbar from "./components/Navbar.vue";
</script>