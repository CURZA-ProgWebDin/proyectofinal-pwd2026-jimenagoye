import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from "../stores/auth";

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import("../views/Home.vue"),
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("../views/Login.vue"),
  },
  {
    path: "/registro",
    name: "Registro",
    component: () => import("../views/Registro.vue"),
  },
  {
    path: "/cursos",
    name: "CatalogoCursos",
    component: () => import("../views/CatalogoCursos.vue"),
  },
  {
    path: "/cursos/:id",
    name: "DetalleCurso",
    component: () => import("../views/DetalleCurso.vue"),
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: () => import("../views/Dashboard.vue"),
    meta: { requiereAuth: true },  // esta ruta solo la ven usuarios logueados
  },
  {
    path: "/crear-curso",
    name: "CrearCurso",
    component: () => import("../views/CrearCurso.vue"),
    meta: { requiereAuth: true, rol: "creador" },  // y además exige rol de creador (o admin)
  },
  {
    path: "/admin/usuarios",
    name: "AdminUsuarios",
    component: () => import("../views/AdminUsuarios.vue"),
    meta: { requiereAuth: true, rol: "administrador" },  // solo para administradores
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to) => {
  const auth = useAuthStore();

  // Navigation Guard: si la ruta pide login y no hay token, redirige al login
  if (to.meta.requiereAuth && !auth.isLoggedIn) {
    return { name: "Login" };
  }

  // Si la ruta exige un rol, verifica que el usuario tenga el rol permitido
  if (to.meta.rol) {
    const permitido =
      to.meta.rol === "administrador" ? auth.esAdmin : auth.esCreador;
    if (!permitido) {
      return { name: "Home" };
    }
  }
});

export default router;
