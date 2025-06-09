<template>
    <header class="sticky-top" v-if="$route?.meta?.showNavBar">
        <NavBarComponent />
    </header>
    <router-view />
    <footer class="overflow-hidden" v-if="$route?.meta?.showFooter">
        <hr />
        <FooterComponent class="py-3" />
    </footer>
</template>
<script>
import NavBarComponent from '@/components/NavBarComponent.vue';
import FooterComponent from '@/components/FooterComponent.vue';

export default {
    name: "App",
    data() {
        return {
            //
        };
    },
    components: {
        NavBarComponent,
        FooterComponent
    }
};
</script>
