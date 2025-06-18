<template>
    <nav class="navbar navbar-expand-lg" style="backdrop-filter: blur(50px)">
        <div class="container">
            <div class="w-lg-25">
                <a class="navbar-brand fw-semibold" href="/">Arcola AI</a>
            </div>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse w-lg-50" id="navbarNav">
                <ul class="navbar-nav mx-auto gap-lg-3 text-center" style="font-size: 0.9rem">
                    <li class="nav-item" v-for="link in navLinks">
                        <RouterLink class="nav-link" :class="$route.path == link[1] ? 'active' : ''" :aria-current="$route.path == link[1] ? 'page' : ''" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
                <!-- Android -->
                <div class="d-flex d-lg-none w-100">
                    <ProfileBarComponent v-if="isLoggedIn" />
                    <div class="d-flex align-items-center justify-content-center w-100" v-else>
                        <RouterLink class="btn btn-sm px-3 rounded-2 btn-login" to="/login">Login</RouterLink>
                        <RouterLink class="btn btn-sm px-3 rounded-2 btn-outline-light" to="/register">Register</RouterLink>
                    </div>
                </div>
            </div>
            <!-- Desktop -->
            <div class="w-lg-25 d-none d-lg-flex align-items-center justify-content-end">
                <ProfileBarComponent v-if="isLoggedIn" />
                <div class="d-flex" v-else>
                    <RouterLink class="btn btn-sm px-3 rounded-2 btn-login" to="/login">Login</RouterLink>
                    <RouterLink class="btn btn-sm px-3 rounded-2 btn-outline-light" to="/register">Register</RouterLink>
                </div>
            </div>
        </div>
    </nav>
</template>
<style scoped>
.btn-login:hover {
    border-color: transparent !important;
}
</style>
<style>
@media (min-width: 992px) {
    .w-lg-25 {
        width: 25% !important;
    }
    .w-lg-50 {
        width: 50% !important;
    }
}
</style>
<script>
import ProfileBarComponent from "@/components/ProfileBarComponent.vue";

export default {
    name: "NavBarComponent",
    data() {
        return {
            navLinks: [
                ["Home", "/"],
                ["Features", "/features"],
                ["Pricing", "/pricing"],
            ],
        };
    },
    components: {
        ProfileBarComponent,
    },
};
</script>
