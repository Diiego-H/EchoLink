<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />

        <!-- Show a loading spinner while fetching song data -->
        <div v-if="!isLoaded" class="flex">
            <LoadingSpinner class="mx-auto" />
        </div>
        <!-- Song view -->
        <div v-else-if="isLoaded && errorMsg === null" class="flex flex-col mx-auto min-w-full container-main">
            <!-- Banner area -->
            <div class="banner content-block mx-auto w-100 mt-8 mb-2">
                <!-- Inner banner area -->
                <div class="sm:flex min-h-32 relative">
                    <!-- Icon and full title -->
                    <div class="flex items-end">
                        <div class="flex size-32 min-w-10 rounded bg-indigo-400">
                            <MusicalNoteIcon class="p-4 my-auto mx-auto" />
                        </div>
                        <!-- Updated artist name and song title display -->
                        <div class="ms-3 flex flex-col items-start">
                            <!-- Artist name with smaller font -->

                            <!-- Song title with custom color -->
                            <p v-if="!isEditing" class="song-title font-bold text-xl text-blue-300 text-left mb-2">
                                {{ song.title }}
                            </p>

                            <p v-if="!isEditing" class="artist-name text-sm text-gray-300 text-left mb-1">
                                <router-link :to="'/users/' + song.artist_name" class="text-gray-300 font-medium">
                                    {{ song.artist_name }}
                                </router-link>
                            </p>

                            <!-- While editing, show artist name as text and title as input field -->
                            <span v-else class="font-bold text-lg text-white mb-2 text-left">
                                <span class="artist-name text-sm text-gray-300">{{ song.artist_name }}</span> -
                                <input class="details-field details-field-editable" v-model="song.title" />
                            </span>
                        </div>

                    </div>

                    <div class="mx-auto my-3"></div>
                    <!-- Spacing between avatar/username and badges, handles both desktop & mobile layouts -->

                    <!-- Edit/delete buttons; in absolute top-right on desktop -->
                    <div class="md:absolute right-0 top-0 d-flex flex-column flex-md-row ml-auto mr-md-0">
                        <button v-if="isOwnSong && isEditing"
                            class="btn btn-red max-w-min text-nowrap mb-2 mb-md-0 me-md-3" @click="deleteSong">
                            <TrashIcon class="icon" />
                            Delete Song
                        </button>
                        <button v-if="isOwnSong" class="btn btn-blue max-w-min text-nowrap" @click="toggleEditMode">
                            <PencilIcon class="icon" />
                            {{ isEditing ? "Save Changes" : "Edit Details" }}
                        </button>
                    </div>
                </div>
            </div>
            <!-- Sources and details -->
            <div class="lg:flex">
                <!-- Sources -->
                <div class="content-block flex flex-grow lg:mr-2">
                    <div class="flex flex-column w-100">
                        <h2 v-if="!isEditing" class="section-header">{{ youtubeVideoID ? 'Listen on YouTube' : 'Listen'
                            }}</h2>
                        <h2 v-else class="section-header">Edit sources</h2>

                        <!-- Source view -->
                        <div v-if="!isEditing" class="flex flex-col w-100 mt-2">
                            <p v-if="song.sources.length == 0" class="text-left">The artist hasn't added any sources for
                                this song yet.</p>

                            <!-- Youtube embed -->
                            <div v-if="youtubeVideoID" class="flex flex-col min-w-full aspect-video">
                                <!-- <router-link :to="`https://www.youtube.com/watch?v=${youtubeVideoID}`" class="text-left">On YouTube</router-link> -->
                                <iframe width="100%" height="100%"
                                    :src="`https://www.youtube.com/embed/${youtubeVideoID}`"
                                    title="YouTube video player" frameborder="0"
                                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                                    referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>
                            </div>
                            <!-- Other sources -->
                            <h2 v-if="youtubeVideoID" class="section-header my-3">Also available on</h2>
                            <div class="flex flex-wrap place-content-center gap-4 mx-auto">
                                <SongSourceCard v-if="spotifyLink" class="bg-green-200 hover:bg-green-300"
                                    :link="spotifyLink" :img="SpotifyLogo" label="On Spotify"></SongSourceCard>
                                <SongSourceCard v-if="soundCloudLink" class="bg-orange-300 hover:bg-orange-400"
                                    :link="soundCloudLink" :img="SoundCloudLogo" label="On SoundCloud"></SongSourceCard>
                                <SongSourceCard v-if="bandcampLink" class="bg-teal-200 hover:bg-teal-300"
                                    :link="bandcampLink" :img="BandcampLogo" label="On Bandcamp"></SongSourceCard>
                                <SongSourceCard v-if="piaproLink" class="bg-pink-300 hover:bg-pink-400"
                                    :link="piaproLink" :img="PiaproLogo" label="On Piapro"></SongSourceCard>
                            </div>
                            <div v-if="otherSources.length > 0" class="flex flex-col mt-2">
                                <p class="text-left">Other sources</p>
                                <ul>
                                    <li v-for="source in otherSources" class="text-left"><a :href="source">{{ source
                                            }}</a></li>
                                </ul>
                            </div>
                        </div>
                        <!-- Source editor -->
                        <div v-else class="flex flex-col w-100">
                            <div v-if="song.sources.length > 0" v-for="source, index in song.sources"
                                class="flex place-items-start w-100">
                                <DetailField class="w-100 pr-3" v-model="song.sources[index]" :id="index.toString()"
                                    inputType="text" :label="`Source ${index + 1}`" :readonly="false"
                                    :pad-between="false" inputFieldClass="text-left" placeholder="Link to source">
                                    <!-- TODO different icon per source? -->
                                    <MusicalNoteIcon class="icon" />
                                </DetailField>
                                <button class="btn-small btn-blue max-w-min text-nowrap my-1"
                                    @click="deleteSource(index)">
                                    <TrashIcon class="icon" />
                                </button>
                            </div>
                            <p v-else class="text-left">You haven't added any sources for this song yet.</p>
                            <button class="btn btn-blue max-w-min text-nowrap mx-auto mt-1" @click="addSource">
                                <PlusIcon class="icon" />
                                Add Source
                            </button>
                        </div>
                    </div>
                </div>

                <div class="my-2"></div> <!-- Used for spacing in column layout (low viewport width) -->

                <!-- Details -->
                <div class="content-block lg:min-w-96 max-h-fit">
                    <h2 class="section-header">Details</h2>
                    <div class="flex">
                        <p><span class="text-nowrap mr-2">
                                <MusicalNoteIcon class="icon" /> Genre:
                            </span></p>
                        <div class="mx-auto"></div>
                        <input type="text" :maxlength="GENRE_MAX_LENGTH" :class="editableFieldClass"
                            class="details-field text-right max-w-min min-w-0" placeholder="Favorite genre"
                            list="genresList" :readonly="!isEditing" v-model="song.genre"></input>
                        <!-- Necessary for browser auto-completion -->
                        <datalist id="genresList">
                            <option v-for="genre in genres" :value="genre" />
                        </datalist>
                    </div>
                    <DetailField id="releaseDate" v-model="song.release_date" label="Release Date"
                        :readonly="!isEditing" input-type="date">
                        <CalendarIcon class="icon" />
                    </DetailField>
                    <DetailField id="album" v-model="song.album" label="Album" :readonly="!isEditing">
                        <BookmarkIcon class="icon" />
                    </DetailField>
                    <!-- TODO duration field -->
                </div>
            </div>
        </div>
        <ErrorPanel v-else header="The song could not be loaded:" :reason="errorMsg"></ErrorPanel>

        <FooterComponent class="footer-light mt-auto" />
    </div>

</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import DetailField from '../components/DetailField.vue';
import SongSourceCard from '../components/SongSourceCard.vue';
import ErrorPanel from '../components/ErrorPanel.vue';
import UserService from '../services/user.js'
import SongService from '../services/song.js'
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import PiaproLogo from '../assets/images/platforms/piapro.svg'
import SpotifyLogo from '../assets/images/platforms/spotify.svg'
import SoundCloudLogo from '../assets/images/platforms/soundcloud.svg'
import BandcampLogo from '../assets/images/platforms/bandcamp.svg'
import { computed, onMounted, ref, watch, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { PencilIcon, MusicalNoteIcon, BookmarkIcon, CalendarIcon, TrashIcon, PlusIcon } from '@heroicons/vue/24/solid'

const router = useRouter()
const route = useRoute()

// TODO ideally this would be fetched from a DB to make it easier to maintain.
const genres = ["Rock", "Pop", "Blues", "Country", "Disco", "Vocaloid", "EDM", "House", "Jazz", "Folk", "Hip hop", "Metal", "Gnomestep", "Nightcore", "Vaporwave", "Synthwave", "Classic"].sort()
const GENRE_MAX_LENGTH = 20

const errorMsg = ref(null) // Error message from song load request.
const isEditing = ref(false) // Whether the song is being edited.
const isLoaded = ref(false) // Whether the page has finished loading - either successfully or with an error.

// Song data. Field names should match the API ones.
const song = reactive({
    title: '',
    album: '',
    genre: '',
    release_date: '',
    artist_name: '',
    sources: [],
})

// Fetches and assigns user data reactive,
// as well as marking the page as loaded and storing error message, if any.
async function fetchSongData() {
    try {
        Object.assign(song, await SongService.get(getSongID()))
    } catch (err) {
        errorMsg.value = (err.response) ? err.response.data.detail : err.message
    } finally {
        // Mark the page as loaded in either case
        isLoaded.value = true
    }
}

function getSongID() {
    return route.params.id
}

function toggleEditMode() {
    // Remove unused source fields
    const newSourceFields = []
    for (const i in song.sources) {
        const source = song.sources[i]
        // Remove duplicate links as well
        if (source !== '' && newSourceFields.findIndex((el) => el === source) === -1) {
            newSourceFields.push(source)
        }
    }
    song.sources = newSourceFields

    // Post to save changes
    if (isEditing.value) {
        SongService.update(getSongID(), song).then(() => {
            Toast.fireSuccess('Details updated')
            // Only exit edit mode if the request was successful,
            // so the user can quickly retry in case of failure.
            isEditing.value = !isEditing.value
        }).catch((err) => {
            Swal.fire({
                title: 'Error',
                text: 'Failed to save changes: ' + ((err.response !== undefined) ? err.response.data.detail : err.message),
                icon: 'error',
            })
        })
    } else {
        // Enter edit mode immediately
        isEditing.value = !isEditing.value
    }
}

function deleteSong() {
    Swal.fire({
        text: "Are you sure you want to delete this song?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes'
    }).then((result) => {
        if (result.isConfirmed) {
            SongService.delete(getSongID()).then(() => {
                Toast.fireSuccess('Song deleted.')
                router.push('/') // Return to homepage
            }).catch((err) => {
                Swal.fire({
                    title: 'Error',
                    text: 'Failed to delete song: ' + (err.response ? err.response.data.detail : err.message),
                    icon: 'error',
                });
            });
        }
    });
}

function addSource() {
    // Don't add a new source if last one hasn't been filled in
    if (song.sources.length === 0 || song.sources[song.sources.length - 1] !== '') {
        song.sources.push('')
    }
}

function deleteSource(index) {
    song.sources.splice(index, 1)
}

function isPiaproLink(link) {
    const regex = RegExp(/http(?:s?):\/\/(?:www\.)?piapro.jp\/t\/([\w\-\_]*)/)
    return regex.test(link)
}

const piaproLink = computed(() => {
    for (const i in song.sources) {
        const source = song.sources[i]
        if (isPiaproLink(source)) {
            return source
        }
    }
    return null
})

function isSpotifyLink(link) {
    const regex = RegExp(/http(?:s?):\/\/(?:www\.)?open\.spotify\.com\/track\/([\w\-\_]*)/)
    return regex.test(link)
}

const spotifyLink = computed(() => {
    for (const i in song.sources) {
        const source = song.sources[i]
        if (isSpotifyLink(source)) {
            return source
        }
    }
    return null
})

function isSoundCloudLink(link) {
    // SoundCloud links include artist username in the path.
    const regex = RegExp(/http(?:s?):\/\/(?:www\.)?soundcloud\.com\/[\w\-\_]+\/([\w\-\_]*)/)
    return regex.test(link)
}

const soundCloudLink = computed(() => {
    for (const i in song.sources) {
        const source = song.sources[i]
        if (isSoundCloudLink(source)) {
            return source
        }
    }
    return null
})

function isBandcampLink(link) {
    // Bandcamp links include artist username in the path.
    const regex = RegExp(/http(?:s?):\/\/(\w+\.)?bandcamp\.com\/track\/([\w\-\_]*)/)
    return regex.test(link)
}

const bandcampLink = computed(() => {
    for (const i in song.sources) {
        const source = song.sources[i]
        if (isBandcampLink(source)) {
            return source
        }
    }
    return null
})

function isYoutubeLink(link) {
    const regex = RegExp(/http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?/) // Source: https://stackoverflow.com/a/3726073
    return regex.test(link)
}

const youtubeVideoID = computed(() => {
    const regex = RegExp(/http(?:s?):\/\/(?:www\.)?youtu(?:be\.com\/watch\?v=|\.be\/)([\w\-\_]*)(&(amp;)?‌​[\w\?‌​=]*)?/) // Source: https://stackoverflow.com/a/3726073
    for (const i in song.sources) {
        const source = song.sources[i]
        const match = regex.exec(source)
        if (match) {
            return match[1]
        }
    }
    return null
})

const otherSources = computed(() => {
    return song.sources.filter((source) => {
        // Looks stupid but there's no reason to overengineer
        return !isYoutubeLink(source) && !isSpotifyLink(source) && !isBandcampLink(source) && !isPiaproLink(source) && !isSoundCloudLink(source)
    })
})

const isOwnSong = computed(() => {
    return UserService.isLoggedIn() && song.artist_name === UserService.getCurrentUsername()
})

const editableFieldClass = computed(() => {
    return {
        "details-field-editable": isEditing.value,
    }
})

// Refetch song data when navigating to another song from this page (ex. directly rewriting the URL or using the header button)
// This is necessary as the component won't be recreated, thus onMounted() won't fire.
watch(
    () => route.params,
    (newId) => {
        fetchSongData(newId)
    }
)

// Fetch song data when the page is accessed from another one.
onMounted(function () {
    fetchSongData(getSongID())
})

</script>

<style scoped>
.container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    /* Align items to the top */
    min-height: 100vh;
    /* Ensure the container takes the full height of the viewport */
}

.btn {
    @apply font-bold py-3 px-4 rounded;
}

.btn-small {
    @apply font-bold py-2 px-2 rounded;
}

.btn-blue {
    @apply bg-blue-500 text-white;
}

.btn-blue:hover,
.btn-blue:focus {
    @apply bg-blue-700;
}

.btn-red {
    @apply bg-red-500 text-white;
}

.btn-red:hover,
.btn-red:focus {
    @apply bg-red-700;
}

.btn-delete {
    @apply bg-blue-500 text-white;
}

.btn-delete:hover,
.btn-delete:focus {
    @apply bg-red-700;
}

.icon {
    @apply h-4 inline
}

.badge {
    @apply max-h-max mx-1 rounded-md select-none text-white
}

.container {
    width: 100vw;
}

.banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover
}

.content-block {
    @apply p-4 border-2 rounded-lg border-indigo-100 bg-indigo-200
}

.section-header {
    @apply text-left font-bold text-xl
}

.details-field {
    /* Padding is used for nicer spacing to the input field boundaries; it's declared in this field as well to prevent the text from changing position when toggling edit mode. */
    @apply px-2 bg-transparent max-h-min
}

.details-field::placeholder {
    @apply text-gray-400
}

.details-field-editable {
    @apply bg-gray-50 border border-gray-300 rounded-lg
}

.center-swal-popup {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px;
    /* Esto puede ser ajustado si es necesario */
    min-width: 320px;
    /* Un ancho mínimo para la ventana emergente */
    max-width: 600px;
    /* Ancho máximo de la ventana emergente */
    width: 90%;
    /* Puedes ajustarlo según lo que prefieras */
}

@media (max-width: 900px) {
    .container-main {
        width: 90%;
        /* Full viewport width for small screens */
        height: auto;
        /* Full viewport height for small screens */
        margin-top: 10vh;
        /* Remove margin for full screen effect */
        border-radius: 0;
        /* Remove border radius for full screen effect */
    }

}

.artist-name {
    font-size: 0.875rem; /* Small font size */
    color: #d1d5db; /* Light gray (tailwind text-gray-300) */
}

.song-title {
    font-size: 1.25rem; /* Large font size */
    color: #93c5fd; /* Light blue (tailwind text-blue-300) */
}

</style>