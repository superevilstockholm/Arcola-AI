<template>
    <section class="vh-100 position-relative overflow-hidden">
        <div class="position-absolute w-100 h-100 p-0 m-0 z-n1">
            <div class="ratio ratio-1x1 w-100 rounded-circle bg-body" style="transform: translateY(25%); filter: blur(100px)"></div>
        </div>
        <div class="container h-100">
            <div class="h-100 w-100 d-flex align-items-center justify-content-center">
                <div class="card px-3 py-4 bg-transparent border-1 col-12 col-md-8 col-lg-5 rounded-3" style="backdrop-filter: blur(10px)">
                    <div class="card-body">
                        <h4 class="card-title text-center">Register</h4>
                        <form @submit.prevent="handleRegister" class="mt-4">
                            <div class="mb-3">
                                <label for="username" class="form-label p-0 m-0">Username</label>
                                <input type="text" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="username" v-model="form.username" minlength="5" maxlength="50" required />
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label p-0 m-0">Email</label>
                                <input type="email" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="email" v-model="form.email" required />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label p-0 m-0">Password</label>
                                <input type="password" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="password" v-model="form.password" minlength="8" maxlength="64" required />
                            </div>
                            <p class="p-0 m-0" style="font-size: 0.9rem">
                                Already have an account?
                                <RouterLink to="/login">Login</RouterLink>
                            </p>
                            <p class="text-danger p-0 m-0 mt-2" style="font-size: 0.9rem">{{ errorMsg }}</p>
                            <button type="submit" class="btn btn-outline-light w-100 mt-2">Register</button>
                        </form>
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

export default {
    name: "RegisterView",
    data() {
        return {
            form: {
                username: "",
                email: "",
                password: "",
            },
            errorMsg: "",
        };
    },
    async mounted() {
        if (await useUserDataStore().isLoggedInCheck()) {
            this.$router.push("/dashboard");
        }
    },
    methods: {
        async handleRegister() {
            await axios
                .post("/api/register", this.form, { headers: { "Content-Type": "application/json" } })
                .then(async (response) => {
                    if (response.status == 200) {
                        if (await response.data?.status) {
                            if ((await response.data?.message) == "User registered successfully") {
                                this.$router.push("/login");
                            }
                        }
                    }
                })
                .catch(async (error) => {
                    if (error.response?.status == 409) {
                        this.errorMsg = await error.response?.data?.message;
                    }
                });
        },
    },
};
</script>
