<template>
    <section class="section artists pb-0 pt-3">
        <div class="container">
            <!-- Header -->
            <div v-if="showHeader" class="row justify-content-center">
                <div class="col-12 col-xl-8">
                    <div data-wow-duration="600ms" data-wow-delay="300ms" class="section__header wow fadeInUp">
                        <h2 ref="artistsHeader" class="h2">Artists</h2>
                    </div>
                </div>
            </div>

            <!-- Loading Spinner -->
            <div v-if="isLoading" class="loading-spinner-container">
                <LoadingSpinner />
            </div>

            <!-- Artist Carousel -->
            <div v-else class="artist-carousel mt-4">
                <Flicking
                    ref="carousel"
                    :options="{ gap: 30, align: 'center', circular: true }"
                    class="carousel-with-blur"
                    @changed="onSlideChange"
                >
                    <div
                        v-for="artist in artists"
                        :key="artist.username"
                        class="artist-card fade-slide-animation"
                    >
                        <ArtistComponent @edited="handleArtistEdited" :artist="artist" />
                    </div>
                </Flicking>

                <!-- Pagination Circles -->
                <div class="pagination-dots">
                    <span
                        v-for="(artist, index) in artists"
                        :key="index"
                        :class="{ active: currentSlide === index }"
                        class="dot"
                        @click="goToSlide(index)"
                    ></span>
                </div>

                <!-- Navigation Buttons -->
                <div class="carousel-navigation">
                    <button @click="prevSlide" class="nav-button prev-button">
                        <i class="fas fa-chevron-left"></i>
                    </button>
                    <button @click="nextSlide" class="nav-button next-button">
                        <i class="fas fa-chevron-right"></i>
                    </button>
                </div>
            </div>
        </div>
    </section>
</template>

<script>
import { defineComponent, ref } from 'vue';
import Flicking from '@egjs/vue3-flicking';
import '@egjs/vue3-flicking/dist/flicking.css';
import ArtistComponent from './ArtistComponent.vue';
import ListenerService from '../services/listener.js';
import fixedImage from '../assets/images/cara1.jpg';
import LoadingSpinner from '../components/LoadingSpinner.vue';

export default defineComponent({
    components: {
        Flicking,
        ArtistComponent,
        LoadingSpinner,
    },
    data() {
        return {
            artists: ref([]),
            currentSlide: 0, // Track the current slide
            isLoading: true, // Track loading state
        };
    },
    methods: {
        async fetchArtists() {
            try {
                const data = await ListenerService.getPreferences();
                this.artists = data.map((artist) => ({
                    ...artist,
                    image: artist.image_url || fixedImage,
                }));
            } catch (error) {
                console.error('Error fetching artists:', error);
            } finally {
                this.isLoading = false; // Stop loading spinner
            }
        },

        async updateCanAsk(index, updatedArtist) {
            const artist = this.artists[index];
            try {
                updatedArtist.can_ask = await ListenerService.canAsk(artist.username);
                this.artists[index] = { ...updatedArtist };
                return this.artists[index].can_ask;
            } catch (err) {
                console.error('Error fetching canAsk:', err);
                return false;
            }
        },

        handleArtistEdited(updatedArtist) {
            const index = this.artists.findIndex((artist) => artist.username === updatedArtist.username);
            if (index !== -1) {
                const artist = this.artists[index];
                if (!artist.is_following && updatedArtist.is_following) {
                    this.updateCanAsk(index, updatedArtist);
                }
                if (!updatedArtist.is_following) {
                    updatedArtist.can_ask = false;
                }
                this.artists[index] = updatedArtist;
            }
        },

        onSlideChange(e) {
            this.currentSlide = e.index; // Update the current slide index
        },

        goToSlide(index) {
            this.$refs.carousel.moveTo(index); // Navigate to the selected slide
        },

        prevSlide() {
            this.$refs.carousel.prev(); // Navigate to the previous slide
        },

        nextSlide() {
            this.$refs.carousel.next(); // Navigate to the next slide
        },
    },
    props: {
        showHeader: Boolean,
    },
    created() {
        this.fetchArtists();
    },
});
</script>

<style scoped>
.artist-card {
    position: relative;
    height: 400px;
    width: 400px;
    margin: 0 30px;
    transition: transform 0.5s ease, opacity 0.5s ease;
}

.artist-card.fade-slide-animation {
    opacity: 0;
    transform: translateY(20px);
    animation: fadeSlideIn 0.6s forwards;
}

@keyframes fadeSlideIn {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

.carousel-with-blur {
    position: relative;
    max-width: 1000px;
    margin: 0 auto;
    -webkit-mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    mask-image: linear-gradient(to right, transparent 0%, black 10%, black 90%, transparent 100%);
    -webkit-mask-repeat: no-repeat;
    mask-repeat: no-repeat;
    -webkit-mask-size: 100% 100%;
    mask-size: 100% 100%;
}

.flicking-viewport {
    overflow: visible;
}

.flicking-camera {
    display: flex;
    gap: 30px;
}

.artist-carousel {
    margin-top: 20px;
    padding: 10px;
    max-width: 1000px;
    margin-left: auto;
    margin-right: auto;
}

.pagination-dots {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}

.dot {
    height: 12px;
    width: 12px;
    margin: 0 5px;
    background-color: #ccc;
    border-radius: 50%;
    display: inline-block;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.dot.active {
    background-color: #000;
}

.carousel-navigation {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.nav-button {
    background: none;
    border: none;
    font-size: 24px;
    cursor: pointer;
    color: #000;
    transition: color 0.3s ease;
}

.nav-button:hover {
    color: #555;
}

.loading-spinner-container {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 400px;
}

@media (max-width: 768px) {
    .artist-card {
        height: 300px;
        width: 300px;
    }

    .carousel-with-blur {
        max-width: 100%;
    }
}
</style>