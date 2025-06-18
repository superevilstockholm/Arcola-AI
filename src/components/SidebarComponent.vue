<template>
    <!-- Navbar untuk mobile -->
    <nav class="navbar navbar-dark d-lg-none sticky-top" style="backdrop-filter: blur(10px)">
        <div class="container">
            <a class="navbar-brand d-flex align-items-center fw-semibold gap-1 py-0 my-0" href="/">
                <div class="d-flex align-items-center gap-1">
                    {{ webBrandName }}
                    <span class="text-primary">{{ webBrandCategory }}</span>
                </div>
            </a>
            <button class="navbar-toggler" type="button" data-bs-toggle="offcanvas" data-bs-target="#sidebarMenu">
                <span class="navbar-toggler-icon"></span>
            </button>
        </div>
    </nav>
    <!-- Sidebar Reusable: Offcanvas (mobile) dan static (desktop) -->
    <div class="offcanvas offcanvas-start d-lg-none bg-transparent" style="backdrop-filter: blur(10px)" tabindex="-1" id="sidebarMenu">
        <div class="offcanvas-header">
            <h5 class="offcanvas-title">Menu</h5>
            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="offcanvas"></button>
        </div>
        <div class="offcanvas-body">
            <SidebarMenuComponent />
        </div>
    </div>
    <!-- Sidebar untuk desktop -->
    <div class="d-none d-lg-block vh-100 position-fixed border-end overflow-hidden" style="width: 200px">
        <div class="p-3">
            <a class="navbar-brand d-flex align-items-center fs-4 fw-semibold gap-1 py-0 mt-0 mb-4" href="/">
                <div class="d-flex align-items-center gap-1">
                    {{ webBrandName }}
                    <span class="text-primary">{{ webBrandCategory }}</span>
                </div>
            </a>
            <SidebarMenuComponent />
        </div>
    </div>
</template>
<script>
import SidebarMenuComponent from "@/components/SidebarMenuComponent.vue";

export default {
    name: "SidebarComponent",
    data() {
        return {
            webBrandName: "Arcola",
            webBrandCategory: "AI"
        };
    },
    components: {
        SidebarMenuComponent,
    }
};
</script>
