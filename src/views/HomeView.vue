<template>
    <section class="position-relative overflow-hidden p-0 m-0" style="height: 579px">
        <!-- Hero Section -->
        <div class="position-absolute w-100 h-100 p-0 m-0 top-50 left-0 z-n1">
            <div class="container">
                <div class="d-flex align-items-center justify-content-center">
                    <div class="w-75 rounded-circle bg-light p-0 m-0 ratio ratio-1x1" style="filter: blur(100px); opacity: 30%"></div>
                </div>
            </div>
        </div>
        <div class="w-100 top-100 left-0 position-absolute" style="height: 35px; background: linear-gradient(to top, rgba(0, 0, 0, 1), rgba(0, 0, 0, 0)); transform: translateY(-35px)"></div>
        <div class="container h-100 py-0 my-0">
            <div class="h-100 w-100 d-flex align-items-center justify-content-center">
                <div class="d-flex flex-column w-100 w-md-75 w-lg-50 text-center">
                    <h6 class="px-3 py-1 mx-auto rounded-pill border border-light d-inline" style="letter-spacing: 3px; font-size: 0.9rem; box-shadow: inset 0 0 10px 0 rgba(255, 255, 255, 0.5)">Bring Your Creativity into Reality with</h6>
                    <h1 class="fw-bold display-4" style="letter-spacing: 2px">Arcola AI</h1>
                    <p class="lead fw-medium" style="font-size: 1rem">Explore the power of AI in one platform - start from intelligent chat, image generator, and document editor integrated with AI.</p>
                    <div class="d-flex align-items-center justify-content-center gap-2">
                        <RouterLink to="/login" class="btn btn-sm fw-semibold px-3 btn-light d-flex align-items-center gap-2">
                            Try Now
                            <i class="bi bi-arrow-right"></i>
                        </RouterLink>
                        <RouterLink to="/features" class="btn btn-sm fw-semibold px-3 btn-outline-light d-flex align-items-center gap-2">
                            See Features
                            <i class="bi bi-book-half"></i>
                        </RouterLink>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <section>
        <!-- Dashboard Preview Section -->
        <div class="container my-5 py-5">
            <div class="row">
                <div class="col-lg-7 p-3 p-lg-5 pt-lg-3">
                    <div class="h-100 w-100 d-flex flex-column justify-content-center p-0 m-0">
                        <h1 class="display-5 fw-bold lh-1">All in one interactive dashboard</h1>
                        <p class="lead fw-normal" style="font-size: 1rem;">Quickly design and customize responsive mobile-first sites with Bootstrap, the world's most popular front-end open source toolkit, featuring Sass variables and mixins, responsive grid system, extensive prebuilt components, and powerful JavaScript plugins.</p>
                        <div class="d-grid gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3">
                            <button type="button" class="btn btn-sm btn-light btn-lg px-4 me-md-2 fw-bold">Primary</button>
                            <button type="button" class="btn btn-sm btn-outline-light btn-lg px-4">Default</button>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg">
                    <img class="rounded-lg-3" src="https://getbootstrap.com/docs/5.0/examples/heroes/bootstrap-docs.png" alt="" width="720" />
                </div>
            </div>
        </div>
    </section>
</template>
<style scoped>
@media (min-width: 768px) {
    .w-md-75 {
        width: 75% !important;
    }
}
@media (min-width: 992px) {
    .w-lg-50 {
        width: 50% !important;
    }
}
</style>
<script>
export default {
    name: "HomeView",
    data() {
        return {
            //
        };
    },
};
</script>
