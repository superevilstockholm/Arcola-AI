<template>
    <div v-if="show" :class="{ 'd-block': show }" style="display: none;">
        <div class="container">
            <h4>Settings</h4>
        </div>
    </div>
</template>
<script>
import { useUserDataStore } from '@/store/UserDataStore';

export default {
    name: "DashboardView",
    data() {
        return {
            show: false
        }
    },
    async mounted() {
        if (!(await useUserDataStore().isLoggedInCheck())) {
            this.$router.push("/login");
        }
        this.show = true;
    }
}
</script>