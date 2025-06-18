import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const routes = [
    {
        path: "/",
        name: "home",
        component: HomeView,
        meta: {
            showNavBar: true,
            showFooter: true,
            showSideBar: false,
        },
    },
    {
        path: "/features",
        name: "Features",
        component: () => import("@/views/FeaturesView.vue"),
        meta: {
            showNavBar: true,
            showFooter: true,
            showSideBar: false,
        },
    },
    {
        path: "/pricing",
        name: "Pricing",
        component: () => import("@/views/PricingView.vue"),
        meta: {
            showNavBar: true,
            showFooter: true,
            showSideBar: false,
        },
    },
    {
        path: "/login",
        name: "login",
        component: () => import("@/views/LoginView.vue"),
        meta: {
            showNavBar: false,
            showFooter: false,
            showSideBar: false,
        },
    },
    {
        path: "/register",
        name: "register",
        component: () => import("@/views/RegisterView.vue"),
        meta: {
            showNavBar: false,
            showFooter: false,
            showSideBar: false,
        },
    },
    {
        path: "/dashboard",
        name: "dashboard",
        component: () => import("@/views/DashboardView.vue"),
        meta: {
            showNavBar: false,
            showFooter: false,
            showSideBar: true,
        },
    },
    {
        path: "/settings",
        name: "settings",
        component: () => import("@/views/SettingsView.vue"),
        meta: {
            showNavBar: false,
            showFooter: false,
            showSideBar: true,
        },
    },
];

const router = createRouter({
    history: createWebHistory(process.env.BASE_URL),
    routes,
});

export default router;
