<template>
    <header class="sticky-top" v-if="$route?.meta?.showNavBar">
        <NavBarComponent />
    </header>
    <SidebarComponent v-if="$route?.meta?.showSideBar" />
    <router-view :class="{ 'ms-lg-200px': $route?.meta?.showSideBar }" />
    <footer class="overflow-hidden" v-if="$route?.meta?.showFooter">
        <hr />
        <FooterComponent class="py-3" />
    </footer>
</template>
<style scoped>
@media (min-width: 992px) {
    .ms-lg-200px {
        margin-left: 200px !important;
    }
}
</style>
<script>
import NavBarComponent from "@/components/NavBarComponent.vue";
import FooterComponent from "@/components/FooterComponent.vue";
import SidebarComponent from "@/components/SidebarComponent.vue";
import axios from "axios";

// For ngrok
axios.defaults.headers.common["ngrok-skip-browser-warning"] = "69420";

export default {
    name: "App",
    data() {
        return {
            //
        };
    },
    components: {
        NavBarComponent,
        FooterComponent,
        SidebarComponent,
    },
};
</script>