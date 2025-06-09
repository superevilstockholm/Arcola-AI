<template>
    <div class="container">
        <div class="row mb-3">
            <div class="col-12 col-md-12 col-lg-6">
                <h4 class="fw-semibold">Arcola AI 🤖</h4>
                <p class="text-muted" style="font-size: 0.9rem;">Arcola AI is an artificial intelligence platform that helps you increase productivity, creativity and work efficiency through modern technologies.</p>
            </div>
            <div class="col-12 col-md-4 col-lg-2">
                <h6 class="fw-semibold">Follow Us</h6>
                <ul class="list-unstyled text-muted" style="font-size: 0.9rem;">
                    <li v-for="link in socialLinks">
                        <RouterLink class="nav-link footer-nav-link" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
            </div>
            <div class="col-12 col-md-4 col-lg-2">
                <h6 class="fw-semibold">Contact Us</h6>
                <ul class="list-unstyled text-muted" style="font-size: 0.9rem;">
                    <li v-for="link in contactLinks">
                        <RouterLink class="nav-link footer-nav-link" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
            </div>
            <div class="col-12 col-md-4 col-lg-2">
                <h6 class="fw-semibold">Pages</h6>
                <ul class="list-unstyled text-muted" style="font-size: 0.9rem;">
                    <li v-for="link in navLinks">
                        <RouterLink class="nav-link footer-nav-link" :to="link[1]">{{ link[0] }}</RouterLink>
                    </li>
                </ul>
            </div>
        </div>
        <div class="row">
            <h6 class="text-center text-muted">Copyright &copy; 2025 Arcola AI. All rights reserved.</h6>
        </div>
    </div>
</template>
<style scoped>
.footer-nav-link {
    display: inline-block;
    transition: all 0.2s ease-in-out;
}
.footer-nav-link:hover {
    color: var(--bs-body) !important;
    filter: brightness(2);
    transform: translateX(5px) scale(1.1);
}
</style>
<script>
export default {
    name: "FooterComponent",
    data() {
        return {
            socialLinks: [
                ["Facebook", "https://www.facebook.com/"],
                ["Twitter", "https://www.twitter.com/"],
                ["Instagram", "https://www.instagram.com/"],
                ["Linkedin", "https://www.linkedin.com/"],
            ],
            contactLinks: [
                ["Email", "mailto:6oN9I@example.com"],
                ["Phone", "tel:+1234567890"],
                ["Address", "https://www.google.com/maps"],
            ],
            navLinks: [
                ["Home", "/"],
                ["Features", "/features"],
                ["Pricing", "/pricing"],
            ],
        };
    },
};
</script>
