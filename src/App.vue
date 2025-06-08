<template>
    <header class="sticky-top">
        <NavBarComponent />
    </header>
    <router-view />
</template>
<script>
import NavBarComponent from './components/NavBarComponent.vue';

export default {
    name: "App",
    data() {
        return {
            //
        };
    },
    components: {
        NavBarComponent
    }
};
</script>
