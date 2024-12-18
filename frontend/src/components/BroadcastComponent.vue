<template>
    <div>
        <section class="section broadcast py-0">
            <div class="container">
                <div class="row">
                    <div class="col-12 fix-scroll">
                        <!-- Listener upsells -->
                        <h2 id="learnMore" class="h-24"></h2> <!-- Intentionally left blank. Serves as navigation anchor only. -->
                        <UpsellBlock id="learnMore" header="Connect with artists" text="On EchoLink, you're closer to your favorite artists than ever before. Follow them to stay in touch with their latest releases and ask them questions to learn more about them." :img="QuestionsImg" />
                        <UpsellBlock header="Discover music and artists" text="Browse thousands of songs and artists on EchoLink to expand your musical interests. You can search songs and artists by genre to find ones matching your favorite vibes." :img="TracksImg" :reverse="true" />

                        <!-- Artist upsells -->
                        <h2 class="section-header w-100">EchoLink for artists</h2>
                        <UpsellBlock header="Grow your fanbase" text="Join EchoLink to let your music reach thousands of fans worldwide. Engage with them by answering their questions, track your performance metrics and climb the ranks to become famous." :img="ArtistDashboardImg" />
                    </div>
                </div>
            </div>
        </section>
    </div>
</template>

<script setup>
import QuestionsImg from "../assets/images/landing_page/question.png"
import TracksImg from "../assets/images/landing_page/tracks.png"
import ArtistDashboardImg from "../assets/images/landing_page/artist_dashboard.png"
</script>

<script>
import UpsellBlock from "../components/UpsellBlock.vue"

export default {
    name: "BroadcastComponent",
    methods: {

    },
    components: {
        "UpsellBlock": UpsellBlock,
    }
};
</script>

<style scoped>
.section-header {
    @apply rounded-xl my-5 p-3 min-w-80 text-nowrap text-white mx-auto;
    background: rgb(116,109,233);
    background: linear-gradient(52deg, rgba(116,109,233,1) 0%, rgba(36,79,82,0.908000700280112) 64%, rgba(76,67,255,1) 100%);
}
</style>