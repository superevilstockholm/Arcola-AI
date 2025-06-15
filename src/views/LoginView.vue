<template>
    <LoadingComponent v-if="isLoading" />
    <section class="vh-100 position-relative overflow-hidden" v-else>
        <div class="position-absolute w-100 h-100 p-0 m-0 z-n1">
            <div class="ratio ratio-1x1 w-100 rounded-circle bg-body" style="transform: translateY(25%); filter: blur(100px)"></div>
        </div>
        <div class="container h-100">
            <div class="h-100 w-100 d-flex align-items-center justify-content-center">
                <div class="card px-3 py-4 bg-transparent border-1 col-12 col-md-8 col-lg-5 rounded-3" style="backdrop-filter: blur(10px)">
                    <div class="card-body">
                        <h4 class="card-title text-center">Login</h4>
                        <form @submit.prevent="handleLogin" class="mt-4">
                            <div class="mb-3">
                                <label for="username" class="form-label p-0 m-0">Username</label>
                                <input type="text" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="username" v-model="form.username" minlength="5" maxlength="50" required />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label p-0 m-0">Password</label>
                                <input type="password" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="password" v-model="form.password" minlength="8" maxlength="64" required />
                            </div>
                            <p class="p-0 m-0" style="font-size: 0.9rem">
                                Dont have an account?
                                <RouterLink to="/register">Register</RouterLink>
                            </p>
                            <p class="text-danger p-0 m-0 mt-2" style="font-size: 0.9rem">{{ errorMsg }}</p>
                            <button type="submit" class="btn btn-light w-100 mt-2">Login</button>
                        </form>
                        <div class="d-flex align-items-center text-muted my-3">
                            <hr class="flex-grow-1 me-2">
                            <span class="small">OR</span>
                            <hr class="flex-grow-1 ms-2">
                        </div>
                        <div class="d-flex align-items-center justify-content-around">
                            <button class="btn btn-light rounded-circle p-0 m-0" data-bs-toggle="tooltip" data-bs-title="Login with Google" data-bs-placement="bottom"><i class="bi bi-google m-0 p-2 fs-3 text-danger"></i></button>
                            <button class="btn btn-light rounded-circle p-0 m-0" data-bs-toggle="tooltip" data-bs-title="Login with Facebook" data-bs-placement="bottom"><i class="bi bi-facebook m-0 p-2 fs-3 text-primary"></i></button>
                            <button class="btn btn-light rounded-circle p-0 m-0" data-bs-toggle="tooltip" data-bs-title="Login with Phone" data-bs-placement="bottom"><i class="bi bi-phone m-0 p-2 fs-3"></i></button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<style scoped>
input:focus {
    box-shadow: none !important;
}
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active {
    -webkit-background-clip: text;
    -webkit-text-fill-color: var(--bs-body);
}
</style>
<script>
import axios from "axios";
import { useUserDataStore } from "@/store/UserDataStore";
import LoadingComponent from "@/components/LoadingComponent.vue";
import { Tooltip } from "bootstrap/dist/js/bootstrap.bundle.min";

export default {
    name: "RegisterView",
    data() {
        return {
            form: {
                username: "",
                password: "",
            },
            errorMsg: "",
            isLoading: true,
        };
    },
    components: {
        LoadingComponent,
    },
    async mounted() {
        try {
            if (await useUserDataStore().isLoggedInCheck()) {
                this.$router.push("/dashboard");
            }
        } finally {
            this.isLoading = false;
            this.$nextTick(() => {
                const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
                tooltipTriggerList.forEach((tooltipTriggerEl) => {
                    new Tooltip(tooltipTriggerEl);
                });
            });
        }
    },
    methods: {
        async handleLogin() {
            await axios
                .post("/api/login", this.form, { headers: { "Content-Type": "application/json" } })
                .then(async (response) => {
                    if (response.status == 200) {
                        if (await response.data?.status) {
                            if ((await response.data?.message) == "User logged in successfully") {
                                this.$router.push("/dashboard");
                            }
                        }
                    }
                })
                .catch(async (error) => {
                    if (error.response?.status == 401) {
                        this.errorMsg = await error.response?.data?.message;
                    }
                });
        },
    },
};
</script>
