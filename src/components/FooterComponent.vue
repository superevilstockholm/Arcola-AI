<template>
    <div class="container">
        <div class="row mb-3">
            <div class="col-12 col-md-12 col-lg-6">
                <h6 class="fw-semibold">Arcola AI</h6>
                <p style="font-size: 0.9rem;">Lorem ipsum dolor sit amet consectetur adipisicing elit. Obcaecati molestias quasi sint.</p>
            </div>
            <div class="col-12 col-md-4 col-lg-2">
                <h6 class="fw-semibold">Follow Us</h6>
                <ul class="list-unstyled" style="font-size: 0.9rem;">
                    <li v-for="link in navLinks">
                        <RouterLink class="nav-link" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
            </div>
            <div class="col-12 col-md-4 col-lg-2">
                <h6 class="fw-semibold">Contact Us</h6>
                <ul class="list-unstyled" style="font-size: 0.9rem;">
                    <li v-for="link in navLinks">
                        <RouterLink class="nav-link" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
            </div>
            <div class="col-12 col-md-4 col-lg-2">
                <h6 class="fw-semibold">Pages</h6>
                <ul class="list-unstyled" style="font-size: 0.9rem;">
                    <li v-for="link in navLinks">
                        <RouterLink class="nav-link" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
            </div>
        </div>
        <div class="row">
            <h6 class="text-center text-muted">Copyright &copy; 2025 Arcola AI. All rights reserved.</h6>
        </div>
    </div>
</template>
<script>
export default {
    name: "FooterComponent",
    data() {
        return {
            socialLinks: [],
            contactLinks: [],
            navLinks: [
                ["Home", "/"],
                ["Features", "/features"],
                ["Pricing", "/pricing"],
            ],
        };
    },
};
</script>
