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
                <div class="d-flex flex-column gap-1 w-100 w-md-75 w-lg-50 text-center">
                    <h6 class="px-3 py-1 mx-auto rounded-pill border border-light d-inline" style="letter-spacing: 3px; font-size: 0.9rem; box-shadow: inset 0 0 10px 0 rgba(255, 255, 255, 0.5)">Bring Your Creativity into Reality with</h6>
                    <h1 class="fw-bold display-4 text-white" style="letter-spacing: 2px;">Arcola AI</h1>
                    <p class="lead fw-medium" style="font-size: 1rem">Explore the power of AI in one platform - start from intelligent chat, image generator, and document editor integrated with AI.</p>
                    <div class="d-flex align-items-center justify-content-center gap-2">
                        <RouterLink to="/login" class="btn btn-sm fw-semibold px-3 btn-light d-flex align-items-center gap-2 me-md-2">
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
                <div class="col-lg-7">
                    <div class="h-100 w-100 d-flex flex-column justify-content-center p-0 m-0">
                        <h1 class="display-5 fw-bold lh-1 text-white">All-in-One Interactive Dashboard</h1>
                        <p class="lead fw-normal" style="font-size: 1rem;">Manage everything in one place — from AI chat, image generation, to smart document editing. Built with a responsive and modern design powered by Bootstrap and enhanced with powerful tools for productivity.</p>
                        <div class="d-flex gap-2 d-md-flex justify-content-md-start mb-4 mb-lg-3">
                            <RouterLink to="/dashboard" class="btn btn-sm btn-light btn-lg px-4 me-md-2 fw-bold d-flex align-items-center gap-2">Go dashboard <i class="bi bi-arrow-right"></i></RouterLink>
                        </div>
                    </div>
                </div>
                <div class="col-lg-4 offset-lg-1 p-0 overflow-hidden shadow-lg">
                    <img class="rounded-3 border border-light" src="/static/img/dashboard_chatbot_preview.png" alt="" width="720" />
                </div>
            </div>
        </div>
    </section>
    <div class="container">
        <hr>
    </div>
    <section class="py-5">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="fw-bold display-4 text-white">Why Choose Arcola AI?</h2>
                <p class="lead fw-normal text-muted" style="font-size: 1rem;">Discover what makes our platform powerful and unique.</p>
            </div>
            <div class="py-3 d-none d-md-block"></div>
            <div class="row text-center">
                <div class="col-md-4 col-12 mb-4 mb-md-0">
                    <i class="bi bi-lightning-charge-fill display-4 text-warning mb-3"></i>
                    <h5 class="fw-bold fs-4 text-white">Blazing Fast</h5>
                    <p class="text-muted">Experience ultra-fast AI response time and generation — from text to image — without waiting.</p>
                </div>
                <div class="col-md-4 col-12 mb-4 mb-md-0">
                    <i class="bi bi-shield-lock-fill display-4 text-info mb-3"></i>
                    <h5 class="fw-bold fs-4 text-white">Secure by Design</h5>
                    <p class="text-muted">Your data is encrypted and handled with the highest privacy standards and technologies.</p>
                </div>
                <div class="col-md-4 col-12 mb-4 mb-md-0">
                    <i class="bi bi-brush-fill display-4 text-success mb-3"></i>
                    <h5 class="fw-bold fs-4 text-white">Creative Tools</h5>
                    <p class="text-muted">Generate images, edit documents, and chat with AI — all in one dashboard designed for creators.</p>
                </div>
            </div>
        </div>
    </section>
    <div class="container">
        <hr>
    </div>
    <section class="py-5">
        <div class="container">
            <div class="text-center mb-5">
                <h2 class="fw-bold display-4 text-white">What People Say</h2>
                <p class="lead text-muted">Hear from our users how Arcola AI transforms their workflow.</p>
            </div>
            <div class="row">
                <div
                    v-for="(testimonial, index) in testimonialsData"
                    :key="index"
                    class="col-md-4 mb-4"
                >
                    <div class="bg-light bg-opacity-10 rounded-3 p-4 h-100">
                        <div class="d-flex align-items-center gap-3 mb-3">
                            <img
                                :src="`https://randomuser.me/api/portraits/${index % 2 === 0 ? 'men' : 'women'}/${30 + index}.jpg`"
                                class="rounded-circle"
                                width="50"
                                height="50"
                                alt="User Avatar"
                            />
                            <div>
                                <h6 class="mb-0 text-white">{{ testimonial.name }}</h6>
                                <small class="text-muted">{{ testimonial.role }}</small>
                            </div>
                        </div>
                        <div class="mb-2 text-warning">
                            <i
                                v-for="i in 5"
                                :key="i"
                                :class="getStarIcon(testimonial.rating, i)"
                            ></i>
                        </div>
                        <p class="text-muted">{{ testimonial.review }}</p>
                    </div>
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
            testimonialsData: [
                {
                    name: "Michaela Nathania W.",
                    role: "Content Creator",
                    rating: 4.5,
                    review: "Arcola AI helps me create images and text faster than ever. A true all-in-one tool!",
                },
                {
                    name: "Tiffany Shah",
                    role: "Freelance Designer",
                    rating: 4.8,
                    review: "Love the image generation tool. It makes my design work so much easier!",
                },
                {
                    name: "Rizky Aditya",
                    role: "AI Enthusiast",
                    rating: 4.2,
                    review: "Its still improving, but the chat and doc features are already quite solid.",
                },
            ]
        };
    },
    methods: {
        getStarIcon(rating, index) {
            const filled = Math.floor(rating);
            const half = rating - filled >= 0.5;
            if (index <= filled) return "bi bi-star-fill";
            if (index === filled + 1 && half) return "bi bi-star-half";
            return "bi bi-star";
        },
    }
};
</script>
