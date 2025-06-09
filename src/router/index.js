import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
        meta: {
            showNavBar: true,
            showFooter: true
        },
    },
    {
        path: "/login",
        name: "login",
        component: () => import("@/views/LoginView.vue"),
        meta: {
            showNavBar: false,
            showFooter: false
        },
    },
    {
        path: "/register",
        name: "register",
        component: () => import("@/views/RegisterView.vue"),
        meta: {
            showNavBar: false,
            showFooter: false
        },
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
