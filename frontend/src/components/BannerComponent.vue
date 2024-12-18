<template>
    <div>
        <section class="section banner-one bg-img my-2 p-0">
            <div class="container my-auto">
                <div class="row items-gap align-items-center lg:py-20 max-md:flex-col-reverse">
                    <div class="col-12 col-md-10 col-lg-6">
                        <div class="banner-one__content flex flex-col">
                            <h1 class="text-3xl text-left text-bold mb-3 text-indigo-900">The social media for fans and artists</h1>
                            <h2 class="h4 text-left">
                                Connect with your favorite artists and explore their tracks on EchoLink - the social media network that brings fans and musicians closer than ever before.</h2>
                            <div class="section__content-cta mx-auto">
                                <a href="/register" class="btn btn--primary">Join EchoLink</a>
                                <a href="#learnMore" class="btn btn--quaternary">Learn More</a> <!-- The secondary and tertiary button classes are actually white and fully blend in with the background. Lmao -->
                            </div>
                        </div>
                    </div>
                    <div class="col-12 col-lg-6">
                        <div class="banner-one__thumb text-start text-lg-end">
                            <img src="../images/img_dummy1.png" alt="Image" class="wow fadeInUp">
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script>


export default {
    name: "BannerComponent",
    methods: {

    }
};
</script>

<style scoped>
.home-light .banner-one {
    background-image: url('~@/assets/images/banner/banner-one-bg-light.png');
}

.home-dark .banner-one {
    background-image: url('~@/assets/images/banner/banner-one-bg.png');
}
</style>