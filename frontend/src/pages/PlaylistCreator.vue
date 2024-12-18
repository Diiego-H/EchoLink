<template>
    <div class="home-two-light home-light page-container">
        <HeaderComponent />
        
        <!-- Show a loading spinner while fetching user data -->
        <div v-if="!isLoaded" class="flex">
            <LoadingSpinner class="mx-auto" />
        </div>
        <div v-else-if="isLoaded && errorMsg === null" class="form-container max-lg:w-full relative mx-auto py-4 max-lg:px-2 lg:px-4 mt-8 border-3 rounded-lg border-indigo-100 bg-indigo-200">
            <!-- Header, edit and share buttons -->
            <!-- Buttons appear on same line as title on desktop, below on mobile -->
            <div class="lg:flex">
                <div class="mb-3 flex-grow">
                    <h2>{{ (isCreating() ? 'Create Playlist' : (isEditing ? 'Edit Playlist' : fullTitle)) }}</h2>
                </div>
                <div class="flex justify-center items-center">
                    <div v-if="!isCreating()" class="h-12 px-2">
                        <button class="btn btn-edit" @click="share">
                            <LinkIcon class="icon" />
                            Share
                        </button>
                    </div>
                    <div v-if="canEdit" class="h-12 px-2">
                        <button v-if="isEditing" class="btn btn-save" @click="saveChanges">
                            <PencilIcon class="icon" />
                            Save
                        </button>
                        <button v-else class="btn btn-edit" @click="isEditing = !isEditing">
                            <PencilIcon class="icon" />
                            Edit
                        </button>
                    </div>
                </div>
            </div>

            <!-- Form field container -->
            <div v-if="isCreating() || isEditing" class="px-4 mx-auto mb-4">
                <!-- Playlist name -->
                <TextInput label="Playlist Name" :required="true" placeholder="My playlist" input-type="text" :value="playlist.name" @changed="playlist.name = $event"></TextInput>

                <!-- Description -->
                <TextInput label="Description" placeholder="Describe your playlist..." input-type="text" :value="playlist.description" @changed="playlist.description = $event" :multiline="true" :max-length="DESCRIPTION_MAX_LENGTH"></TextInput>

                <!-- Visibility -->
                <OptionSelector v-model="playlist.visibility" :options="VISIBILITY_OPTIONS" label="Visibility" track-by="id" option-label-key="label" :allow-empty="false" :can-search="false"></OptionSelector>
            </div>
            <!-- Read-only details -->
            <div v-else class="px-4 mx-auto mb-3">
                <p>{{ playlist.description }}</p>
            </div>

            <!-- Song list; songs are added after creating a playlist, thus this doesn't appear in the creator view -->
            <SongList v-if="!isCreating()" v-model="playlist.songs" :editable="isEditing" @removed="onSongDeleted($event)" @reordered="onSongsReordered()"></SongList>
            <p class="text-gray-500" v-if="!isCreating() && playlist.songs.length == 0">This playlist has no songs yet.<br>{{ canEdit ? 'Edit the playlist to start adding songs.' : '' }}</p>

            <!-- "Add song" widget -->
            <div v-if="isEditing" class="mt-3">
                <label for="songSelector" class="block text-sm font-medium text-left ml-1 mb-2" >Add song</label>
                <div class="flex items-center">
                    <Multiselect v-model="songToAdd" :options="songs" :track-by="'song_id'" :label="'fullTitle'" :allow-empty="false" :searchable="true" id="songSelector"></Multiselect>
                    <button v-if="isEditing" class="btn btn-save ml-3 mb-0" :disabled="!canAddSong" @click="addSong">
                        <PlusIcon class="icon" />
                        Add
                    </button>
                </div>
            </div>

            <!-- "Create" button -->
            <button v-if="isCreating()" class="btn btn--primary w-100 w-md-60 mt-3" :disabled="!canCreate" @click="createPlaylist">Create</button>
        </div>
        <ErrorPanel v-else header="The playlist could not be loaded:" :reason="errorMsg"></ErrorPanel>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import OptionSelector from '../components/form/OptionSelector.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import SongList from '../components/SongList.vue';
import ErrorPanel from '../components/ErrorPanel.vue';
import PlaylistService from '../services/playlist.js'
import Multiselect from 'vue-multiselect'
import SongService from '../services/song.js'
import UserService from '../services/user.js'
import Toast from '../utilities/toast.js'
import Swal from 'sweetalert2'
import { PencilIcon, PlusIcon, LinkIcon } from '@heroicons/vue/24/solid'
import { useRoute, useRouter } from 'vue-router';
import { computed, reactive, ref, watch, onMounted } from 'vue';

const router = useRouter()
const route = useRoute()

const DESCRIPTION_MAX_LENGTH = 120
// IDs be coherent with the API.
const VISIBILITY_OPTIONS = [
    {id: 'public', label: 'Public'},
    {id: 'private', label: 'Private'},
] 

const playlist = reactive({
    name: '',
    description: '',
    visibility: VISIBILITY_OPTIONS[0], // Default to first option.
    username: 'pip',
    songs: [],
})
const songs = reactive([])
const songToAdd = ref(null)
const isEditing = ref(false)
const errorMsg = ref(null) // Error message from playlist load request.
const isLoaded = ref(false) // Whether the page has finished loading - either successfully or with an error.
const requestPending = ref(false)

function createPlaylist() {
    requestPending.value = true

    // Should be consistent with the API.
    const playlistData = {
        name: playlist.name,
        description: playlist.description,
        visibility: playlist.visibility.id,
    }
    PlaylistService.createPlaylist(playlistData).then((data) => {
        Toast.fireSuccess('Playlist created')
        router.push('/playlists/' + data.playlist_id) // Go to the playlists's page
    }).catch((err) => {
        Swal.fire({
            title: 'Error',
            text: 'Failed to create playlist: ' + err,
            icon: 'error',
        })
    }).finally(() => {
        requestPending.value = false
    })
}

function addSong() {
    const newSong = songToAdd.value

    // Prevent adding a song twice
    if (canAddSong.value) {
        PlaylistService.addSong(route.params.id, newSong).then(() => {
            playlist.songs.push(newSong)
        }).catch((err) => {
            Swal.fire({
                title: 'Error',
                text: 'Failed to add song: ' + ((err.response !== undefined) ? err.response.data.detail : err.message),
                icon: 'error',
            })
        })
    }
}

function onSongDeleted(song) {
    PlaylistService.removeSong(route.params.id, song).catch((err) => {
        Swal.fire({
            title: 'Error',
            text: 'Failed to remove song: ' + ((err.response !== undefined) ? err.response.data.detail : err.message) + '. Please refresh the page.', // This fucking sucks
            icon: 'error',
        })
    })
}

function onSongsReordered() {
    const songIDs = new Array()
    for (const index in playlist.songs) {
        songIDs.push(playlist.songs[index].song_id)
    }
    PlaylistService.reorderSongs(route.params.id, songIDs).catch((err) => {
        Swal.fire({
            title: 'Error',
            text: 'Failed to reorder songs: ' + ((err.response !== undefined) ? err.response.data.detail : err.message) + '. Please refresh the page.', // This fucking sucks
            icon: 'error',
        })
    })
}

const canAddSong = computed(() => {
    const newSong = songToAdd.value
    return newSong !== null && playlist.songs.find((song) => song.song_id === newSong.song_id) === undefined
})

// Updates the details of the playlist only;
// songs are handled separately due to API quirks.
function saveChanges() {
    PlaylistService.update(route.params.id, {
        name: playlist.name,
        description: playlist.description,
        visibility: playlist.visibility.id,
    }).then(() => {
        Toast.fireSuccess('Playlist updated')
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
}

async function share() {
    try {
        const isFirefox = navigator.userAgent.toLowerCase().includes('firefox');

        // No perms are required on Firefox, but it will fail outside of HTTPS
        if (isFirefox) {
            navigator.clipboard.writeText(window.location.href).then(() => {
                Toast.fireSuccess('Link copied to clipboard')
            });
        } else {
            // Ask for permissions first
            navigator.permissions.query({name: "clipboard-write"}).then((result) => {
                if (result.state === "granted" || result.state === "prompt") {
                    navigator.clipboard.writeText(window.location.href).then(() => {
                        Toast.fireSuccess('Link copied to clipboard')
                    });
                }
            });
        }
    } catch {
        Toast.fireError('Failed to copy link')
    }
}

// Fetches and assigns playlist data reactive,
// as well as marking the page as loaded and storing error message, if any.
async function fetchPlaylistData(id) {
    try {
        const newData = await PlaylistService.get(id)
        playlist.name = newData.name
        playlist.description = newData.description
        playlist.visibility = VISIBILITY_OPTIONS.find((el) => el.id === newData.visibility)
        playlist.username = newData.username

        // Yep. I'm expected to go and fetch each song individually. Yep.
        const songs = await SongService.getAll()
        const songsArray = new Array()
        for (const index in newData.songs) {
            songsArray.push(songs.find((el) => el.song_id === newData.songs[index].song_id))
        }

        playlist.songs = songsArray

        // Clear any previous error message so the new playlist is shown
        errorMsg.value = null
    } catch (err) {
        errorMsg.value = (err.response) ? err.response.data.detail : err.message
    } finally {
        // Mark the page as loaded in either case
        isLoaded.value = true
    }
}

async function fetchSongs() {
    try {
        const fetchedSongs = await SongService.getAll()
        // Add an extra field to improve vue-multiselect search support (since it only supports searching by one key)
        for (const index in fetchedSongs) {
            const song = fetchedSongs[index]
            song.fullTitle = `${song.artist_name} - ${song.title}`
        }
        Object.assign(songs, fetchedSongs)
    } catch (err) {
        errorMsg.value = (err.response) ? err.response.data.detail : err.message
    }
}

// Refetch playlist data when navigating to another playlist from this page (ex. directly rewriting the URL)
// This is necessary as the component won't be recreated, thus onMounted() won't fire.
watch(
    () => route.params,
    (newParams) => {
        fetchPlaylistData(newParams.id)
    }
)

// Fetch playlist data when the page is accessed from another one.
onMounted(function () {
    if (!isCreating()) {
        fetchPlaylistData(route.params.id)
    } else {
        isLoaded.value = true
    }
    fetchSongs() // Only needs to be done once (ie. no need to refetch if the URL is rewritten by router). Must be done even if we enter the creator page first, as the component will be re-used when entering the edit page afterwards.
})

const canEdit = computed(() => {
    return !isCreating() && playlist.username === UserService.getCurrentUsername()
})

const canCreate = computed(() => {
    return isCreating() && playlist.name !== '' && !requestPending.value // Disallow sending more requests until each has resolved.
})

function isCreating() {
    return route.params.id === 'new'
}

const fullTitle = computed(() => {
    return `${playlist.name} by ${playlist.username}` // TODO edit to username once we have those accessible
})

</script>

<style scoped>
.page-container {
    width: 100vw;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align items to the top */
    min-height: 100vh; /* Ensure the container takes the full height of the viewport */
}

.form-container {
    box-sizing: border-box; /* Include padding and border in the element's total width and height */
    margin-top: 50px; /* Add some margin to push the form down slightly from the header */
}
@media (min-width: 900px) {
    .form-container {
        width: 800px;
    }
}

.footer-light {
    width: 100vw;
}

.btn-edit {
    @apply font-bold py-3 px-4 rounded;
    @apply bg-blue-500 text-white;
    @apply max-w-min text-nowrap mb-2
}

.btn-edit:hover,
.btn-edit:focus {
    @apply bg-blue-700;
}

.btn-save {
    @apply font-bold py-3 px-4 rounded;
    @apply bg-green-500 text-white;
    @apply max-w-min text-nowrap mb-2
}

.btn-save:hover,
.btn-save:focus {
    @apply bg-green-700;
}

@media (max-width: 768px) {
    .form-container {
        height: auto; /* Full viewport height for small screens */
        margin-top: 10vh; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }

}
</style>