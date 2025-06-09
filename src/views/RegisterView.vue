<template>
    <section class="vh-100">
        <div class="container h-100">
            <div class="h-100 w-100 d-flex align-items-center justify-content-center">
                <div class="card px-3 py-4 bg-transparent border-1 col-12 col-md-8 col-lg-6 rounded-3" style="box-shadow: inset 0 0 15px 1px rgba(255, 255, 255, 0.7); border-color: rgba(var(--bs-body-color-rgb), 0.7);">
                    <div class="card-body">
                        <h4 class="card-title text-center">Register</h4>
                        <form @submit.prevent="handleRegister" class="mt-4">
                            <div class="mb-3">
                                <label for="username" class="form-label">Username</label>
                                <input type="text" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="username" v-model="form.username" minlength="5" maxlength="50" required />
                            </div>
                            <div class="mb-3">
                                <label for="email" class="form-label">Email</label>
                                <input type="email" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="email" v-model="form.email" required />
                            </div>
                            <div class="mb-3">
                                <label for="password" class="form-label">Password</label>
                                <input type="password" class="form-control form-control-sm border-0 bg-transparent border-bottom rounded-0" id="password" v-model="form.password" minlength="8" maxlength="64" required />
                            </div>
                            <p class="text-danger">{{ errorMsg }}</p>
                            <button type="submit" class="btn btn-primary w-100">Register</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </section>
</template>
<script>
import axios from 'axios';

export default {
    name: "RegisterView",
    data() {
        return {
            form: {
                username: "",
                email: "",
                password: "",
                confirmPassword: "",
            },
            errorMsg: ""
        };
    },
    methods: {
        async handleRegister() {
            await axios.post("/api/register", this.form, { headers: { "Content-Type": "application/json" } }).then(async (response) => {
                if (response.status == 200) {
                    if (await response.data?.status) {
                        if (await response.data?.message == "User registered successfully") {
                            this.$router.push("/login");
                        }
                    }
                }
            }).catch(async (error) => {
                if (error.response?.status == 409) {
                    this.errorMsg = await error.response?.data?.message
                }
            })
        }
    }
};
</script>
