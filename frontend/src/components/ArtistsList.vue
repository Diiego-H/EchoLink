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

          <!-- Artist Grid -->
          <div class="artist-grid mt-4">
              <div v-for="artist in artists" :key="artist.username" class="artist-card">
                  <ArtistComponent :artist="artist" />
              </div>
             
          </div>
      </div>
  </section>
</template>

<script>
import { defineComponent } from 'vue';
import ArtistComponent from './ArtistComponent.vue';
import ArtistService from '../services/artist.js'; // Assume this service handles API calls
import fixedImage from '../assets/images/cara1.jpg';

export default defineComponent({
  components: {
      ArtistComponent,
  },
  data() {
      return {
          artists: []
      };
  },
  methods: {
      async fetchArtists() {
          try {
              const data = await ArtistService.getArtistsByAlphabet();
              this.artists = data.map((artist) => ({
                  ...artist,
                  image: artist.image_url || fixedImage,
              }));
          } catch (error) {
              console.error('Error fetching artists:', error);
          }
      }
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
.artist-grid {
  display: grid;
  grid-template-columns: 1fr; /* Default to 1 column */
  gap: 30px;
  max-width: 1000px;
  margin: 0 auto;
  padding: 10px;
}

@media (min-width: 768px) {
  .artist-grid {
      grid-template-columns: repeat(2, 1fr); /* 2 columns for medium screens */
  }
}

@media (min-width: 1200px) {
  .artist-grid {
      grid-template-columns: repeat(3, 1fr); /* 3 columns for large screens */
  }
}

.artist-card {
  position: relative;
  width: 100%; /* Adjust width to fit grid column */
  padding-top: 100%; /* This ensures the card is square by making height proportional to width */
  background-color: #f9f9f9; /* Optional: Add a background color */
  overflow: hidden;
}

.artist-card > * {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.view-all-artists-div {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>