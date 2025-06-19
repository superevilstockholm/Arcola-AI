<template>
    <ul class="nav flex-column gap-2" style="font-size: 0.8rem;">
        <li class="nav-item" v-for="link in sidebarLinks">
            <RouterLink :to="link[1]" class="nav-link d-flex align-items-center gap-1 text-white rounded-2" :class="{ 'text-dark nav-link-active': $route.path == link[1] }">
                <i class="bi" :class="link[2]"></i>
                {{ link[0] }}
            </RouterLink>
        </li>
        <li class="nav-item">
            <button class="logout-btn d-flex text-white align-items-center gap-1 nav-link rounded-2 w-100 fw-semibold" type="button" @click="logout">
                <i class="bi bi-box-arrow-right"></i>
                Logout
            </button>
        </li>
    </ul>
</template>
<style scoped>
.nav-link {
    transition: all 0.2s ease-in-out;
}
.nav-link:hover {
    background-color: rgba(var(--bs-body-color-rgb), 0.1);
}
.nav-link-active {
    background-color: rgba(var(--bs-body-color-rgb), 0.2)!important;
}
.logout-btn:hover {
    color: var(--bs-body-color) !important;
    background-color: rgba(var(--bs-danger-rgb), 0.5) !important;
}
</style>
<script>
import axios from 'axios';
import Swal from 'sweetalert2';

export default {
    name: "SidebarMenuComponent",
    data() {
        return {
            sidebarLinks: [
                ["Dashboard", "/dashboard", "bi-graph-up-arrow"],
                ["Chat Bot", "/chat", "bi-chat-dots"],
                ["Image Generator", "/imgen", "bi-image"],
                ["Settings", "/settings", "bi-gear"]
            ]
        }
    },
    methods: {
        async logout() {
            const result = await Swal.fire({
                title: 'Logout',
                text: "Are you sure you want to logout?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#d33',
                cancelButtonColor: '#3085d6',
                confirmButtonText: 'Logout',
                cancelButtonText: 'Cancel',
                reverseButtons: true
            });
            if (!result.isConfirmed) {
                return;
            }
            await axios.delete("/api/logout", { withCredentials: true }).then(() => { this.$router.push("/login") }).catch(() => { this.$router.push("/login") });
        }
    }
}
</script>