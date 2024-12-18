<template>
    <div class="home-two-light home-light container">

        <HeaderComponent />
        <!-- Set a fixed width for the container -->
        <div class="form-container mx-auto p-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <div class="mb-3">
                <h2>Upload a new track</h2>
            </div>

            <!-- Form field container -->
            <div class="px-4 mx-auto">
                <!-- Basic info -->
                <TextInput label="Title" :required="true" placeholder="Title" input-type="text" :value="songtitle" @changed="songtitle = $event" :warning="titleWarning" :test-id="'field-title'"></TextInput>
                <TextInput label="Album" :required="true" placeholder="Album" input-type="text" :value="album" @changed="album = $event" :warning="albumWarning" :test-id="'field-album'"></TextInput>
                <!--<TextInput label="Genre" :required="true" placeholder="Genre" input-type="text" :value="genre" @changed="genre = $event" :warning="genreWarning" :test-id="'field-genre'"></TextInput>-->
                <div class="mb-4">
                    <div class="flex justify-between items-center">
                        <label for="genre" class="block text-sm font-medium text-gray-900">Genre <span class="text-black-600">*</span></label>                        
                        <p v-if="genreWarning" class="text-sm text-red-600 font-medium mt-1">{{ genreWarning }}</p>
                    </div>
                    <div class="mt-1">
                        <input
                            type="text"
                            id="genre"
                            maxlength="50"
                            class="w-full px-3 py-2 border bg-gray-50 border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                            placeholder="Select a genre"
                            list="genresList"
                            v-model="genre"
                            data-test="field-genre"
                        />
                        <datalist id="genresList">
                            <option v-for="genre in genres" :key="genre" :value="genre" />
                        </datalist>
                    </div>
                </div>


                <TextInput label="Release Date" :required="true" placeholder="Select a date" input-type="date" :value="releaseDate" @changed="releaseDate = $event" :warning="dateWarning" :test-id="'field-release-date'"></TextInput>                
                <hr class="h-divider"/>

                <button class="btn btn--primary w-100 w-md-60" :disabled="!canUpload" @click="uploadTrack" :data-test="'button-uploadTrack'">Upload Track</button>

            </div>
        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import UserService from '../services/user.js'
import SongService from '../services/song.js';
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter()

const songtitle = ref('')
const genre = ref('')
const album = ref('')
const releaseDate = ref('')

const genres = ["Rock", "Pop", "Blues", "Country", "Disco", "Vocaloid", "EDM", "House", "Jazz", "Folk", "Hip hop", "Metal", "Gnomestep", "Nightcore", "Vaporwave", "Synthwave", "Classic"].sort()


function uploadTrack() {
    const username = UserService.getCurrentUsername();
    if (!username) {
    Swal.fire({
        title: 'Error',
        text: 'You need to be logged in to upload a track.',
        icon: 'error',
    });
    return;
    }
    const songInput = {
        title: songtitle.value,
        album: album.value,
        genre: genre.value,
        release_date: releaseDate.value,
        artist_name: username,
    };
    console.log('Song input:', songInput);
    SongService.addSong(songInput).then(() => {
        Toast.fire({
            title: 'Track uploaded successfully!',
            icon: 'success',
        })
        router.push('/')
    }).catch((err) => {
        Swal.fire({
            title: 'Track upload failed',
            text: (err.response !== null) ? err.response.data.detail : err.message,
            icon: 'error',
        })
    })
}
const isTitleValid = computed(() => {
    return (songtitle.value !== '')
})
const isGenreValid = computed(() => {
    return (genre.value !== '')
})
const isAlbumValid = computed(() => {
    return (album.value !== '')
})
const isDateValid = computed(() => {
    return (releaseDate.value !== '')
})
const canUpload = computed(() => {
    return isTitleValid.value && isGenreValid.value && isAlbumValid.value && isDateValid.value
})

// Warnings for invalid fields
const titleWarning = computed(() => {
    if (songtitle.value === '') {
        return 'This field is required';
    }
})
const albumWarning = computed(() => {
    if (album.value === '') {
        return 'This field is required';
    }
})
const genreWarning = computed(() => {
    if (genre.value === '') {
        return 'This field is required';
    }
})
const dateWarning = computed(() => {
    if (releaseDate.value === '') {
        return 'This field is required';
    }
})
</script>


<style scoped>
.container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align items to the top */
    min-height: 100vh; /* Ensure the container takes the full height of the viewport */
}

.form-container {
    width: 600px;
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
    margin-top: 50px; /* Add some margin to push the form down slightly from the header */
}

.footer-light {
    width: 100vw;
}

@media (max-width: 768px) {
    .form-container {
        width: 90vw; /* Full viewport width for small screens */
        height: auto; /* Full viewport height for small screens */
        margin-top: 10vh; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }
}


input::placeholder {
  @apply text-gray-500
}

</style>