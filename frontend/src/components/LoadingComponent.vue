<template>
    <div class="vh-100 vw-100 p-0 m-0 position-fixed top-0 left-0" style="z-index: 99999999999999999;">
        <div class="container w-100 h-100 py-0 my-0">
            <div class="d-flex align-items-center justify-content-center w-100 h-100">
                <div class="spinner-border" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
export default {
    name: "LoadingComponent",
    data() {
        return {
            // 
        }
    },
}
</script>