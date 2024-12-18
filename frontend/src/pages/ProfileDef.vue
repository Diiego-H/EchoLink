<template>
    <div class="home-two-light home-light page-container">
        <HeaderComponent />

        <!-- Show a loading spinner while fetching user data -->
        <div v-if="!isLoaded" class="flex">
            <LoadingSpinner class="mx-auto" />
        </div>
        <!-- Profile view -->
        <div v-else-if="isLoaded && errorMsg === null" class="flex flex-col mx-auto max-w-screen-lg container-main"
            data-test="container-main">
            <!-- Username, badges and banner area -->
            <div class="banner content-block mx-auto w-100 mt-8 mb-2">
                <!-- Inner banner area -->
                <div class="sm:flex min-h-32 relative">
                    <!-- Avatar and username -->                        
                    <div class="flex items-end">
                        <img class="max-w-32 min-w-20 h-auto rounded-3 border-black" :src=" user.image_url" />
                        <div class="ms-3 flex flex-col items-start w-full">
                            <!-- TODO ensure contrast vs banner -->
                            <div class="flex items-center w-full mb-2 space-x-4">
                                <p class="font-bold text-lg text-white mb-2 text-left" data-test="label-username">{{ getUsername() }}</p>
                            </div>

                            <div class="flex max-lg:flex-col gap-2 gap-y-2">
                                <button v-if="!isOwnProfile && isArtist" class="btn btn-blue max-w-min text-nowrap" @click="askQuestion" data-test="button-ask">
                                    <ChatBubbleBottomCenterTextIcon class="icon" />
                                    Ask me something!
                                </button>
                                
                                <button v-if="!isOwnProfile && isArtist && userRole==='listener'" class="btn btn-blue max-w-min text-nowrap" @click="toggleFollow" data-test="button-follow">
                                    <component 
                                        :is="isFollowing ? UserMinusIcon : UserPlusIcon" 
                                        class="icon"
                                    />
                                    {{ isFollowing ? 'Unfollow' : 'Follow'  }}
                                </button>

                            </div>
                        </div>
                    </div>

                    <div class="mx-auto my-3"></div>
                    <!-- Spacing between avatar/username and badges, handles both desktop & mobile layouts -->

                    <!-- "Edit Profile" button; always in top-right -->
                    <div class="absolute right-0 top-0 d-flex flex-column flex-md-row ml-auto mr-md-0">
                        <button v-if="isOwnProfile && isEditing"
                            class="btn btn-red max-w-min text-nowrap mb-2 mb-md-0 me-md-3" @click="deleteAccount"
                            data-test="button-delete">
                            <TrashIcon class="icon" />
                            Delete Account
                        </button>
                        <button v-if="isOwnProfile" class="btn btn-blue max-w-min text-nowrap" @click="toggleEditMode"
                            data-test="button-edit">
                            <PencilIcon class="icon" />
                            {{ isEditing ? "Save Changes" : "Edit Profile" }}
                        </button>
                    </div>
                    <!-- Right area; badges & owner controls -->
                    <div class="flex flex-col items-end">

                        <div class="my-auto"></div>

                        <!-- Badges area -->
                        <div class="flex">
                            <!-- Account type badge -->
                            <!-- TODO modify this once we have other user roles -->
                            <div class="badge bg-indigo-500" v-tooltip="accountTypeBadgeTooltip">
                                <span class="text-white">
                                    <MusicalNoteIcon class="icon" /> {{ roleName }}
                                </span>
                            </div>

                            <!-- Visibility badge -->
                            <!-- Redundant to show this for other users; if their profile is accessible, then it means it's already public (or from a friend user) -->
                            <!-- Artists are considered always public, thus they don't need this widget. -->
                            <div v-if="isOwnProfile && !isArtist" :class="visibilityBadgeClass" class="badge bg-blue-500"
                                @click="toggleVisibility" v-tooltip="visibilityBadgeTooltip"
                                data-test="badge-visibility">
                                
                                <span class="text-white">
                                    <span v-if="!isEditing" class="text-white">
                                        <GlobeAltIcon class="icon" />
                                        {{ user.publicProfile ? "Public Profile" : "Private Profile" }}
                                    </span>
                                    <!-- When editing, show a checkbox instead of the globe icon -->
                                    <span v-else class="flex max-w-fit items-center text-white">
                                        <input class="size-4 mr-1" type="checkbox" v-model="user.publicProfile" />
                                        <!-- When editing, always show this badge as "Public Profile" to clarify the meaning of on/off for the checkbox. -->
                                        Public Profile
                                    </span>
                                </span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Description and details -->
            <div class="lg:flex">
                <!-- Description -->
                <div class="content-block flex flex-grow lg:mr-2">
                    <div class="flex flex-column">
                        <h2 class="section-header">About</h2>
                        <textarea cols="999999" autocomplete="off" autocorrect="on" :class="editableFieldClass"
                            class="details-field text-left flex-grow w-100 min-w-full min-h-60"
                            :maxlength="DESCRIPTION_MAX_LENGTH" :placeholder="isOwnProfile ? 'Describe yourself' : 'No description provided.'" :readonly="!isEditing"
                            v-model="user.description" data-test="field-description"></textarea>
                    </div>
                </div>

                <div class="my-2"></div> <!-- Used for spacing in column layout (low viewport width) -->

                <!-- Details -->
                <div class="content-block lg:min-w-96">
                    <h2 class="section-header">Details</h2>
                    <div class="flex">
                        <p><span class="text-nowrap mr-2">
                                <MusicalNoteIcon class="icon" /> {{ isArtist ? 'Main Genre' : 'Favorite Genre' }}:
                            </span></p>
                        <div class="mx-auto"></div>
                        <input type="text" :maxlength="GENRE_MAX_LENGTH" :class="editableFieldClass"
                            class="details-field text-right max-w-min min-w-0" placeholder="Favorite genre"
                            list="genresList" :readonly="!isEditing" v-model="user.genre"
                            data-test="field-genre"></input>
                        <!-- Necessary for browser auto-completion -->
                        <datalist id="genresList">
                            <option v-for="genre in genres" :value="genre" />
                        </datalist>
                    </div>
                </div>
            </div>
            <div class="my-2"></div>
            <!-- User Playlists -->
            <div class="content-block flex-col">
                <!-- Header -->
                <div class="flex justify-between items-center">
                    <h2 class="section-header">{{ isOwnProfile ? 'My Playlists' : 'Playlists' }}</h2>
                    <button v-if="isOwnProfile" class="btn btn-blue max-w-min text-nowrap ml-auto" @click="goToPlaylistCreator">
                        <PlusIcon class="icon" />
                        Add New Playlist
                    </button>
                </div>
                <!-- Playlist list -->
                <div class="flex flex-col py-3">
                    <div v-for="playlist in visiblePlaylists" class="rounded">
                        <div class="flex items-center echolink-container my-1">
                            <!-- Playlist icon (would be ex. album cover) -->
                            <!-- min-w is necessary to avoid the box being compressed if title is too long -->
                            <div class="flex size-10 min-w-10 rounded bg-indigo-400">
                                <MusicalNoteIcon class="icon-h5 my-auto mx-auto"/>
                            </div>

                            <!-- Playlist title -->
                            <span class="mx-3 text-left">
                                <router-link :to="`/playlists/${playlist.playlist_id}`">{{ playlist.name }}</router-link>
                            </span>

                            <div class="mx-auto"></div>

                            <!-- TODO show song count -->

                            <!-- Delete button -->
                            <button v-if="isOwnProfile" class="btn btn-delete text-nowrap p-2" @click="deletePlaylist(playlist.playlist_id)">
                                <TrashIcon class="icon-h5" />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <!-- Error view -->
        <div v-else class="content-block max-w-sm mx-auto" data-test="container-error">
            <p>The profile could not be loaded:</p>
            <p>{{ errorMsg }}</p>
            <RouterLink to="/">Return to homepage</RouterLink>
        </div>
        <FooterComponent class="footer-light" />
    </div>

</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue';
import UserService from '../services/user.js'
import QuestionService from '../services/question.js'
import PlaylistService from '../services/playlist.js'
import ListenerService from '../services/listener.js'
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import AvatarSvg from '../assets/images/avatar.svg'
import Cookies from 'js-cookie';
import { computed, onMounted, ref, watch, reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { PencilIcon, MusicalNoteIcon, GlobeAltIcon, TrashIcon, PlusIcon, ChatBubbleBottomCenterTextIcon, UserMinusIcon, UserPlusIcon } from '@heroicons/vue/24/solid'

const router = useRouter()
const route = useRoute()

// Max lengths of fields, in characters.
// TODO adjust these to match backend
const DESCRIPTION_MAX_LENGTH = 120
const GENRE_MAX_LENGTH = 20

// TODO ideally this would be fetched from a DB to make it easier to maintain.
const genres = ["Rock", "Pop", "Blues", "Country", "Disco", "Vocaloid", "EDM", "House", "Jazz", "Folk", "Hip hop", "Metal", "Gnomestep", "Nightcore", "Vaporwave", "Synthwave", "Classic"].sort()

const errorMsg = ref(null) // Error message from profile load request.
const isEditing = ref(false) // Whether the profile is being edited.
const isLoaded = ref(false) // Whether the page has finished loading - either successfully or with an error.
const isFollowing = ref(false)
const userRole = ref(null)

// Profile data. Field names should match the API ones.
const user = reactive({
    genre: '',
    description: '',
    visibility: 'public',
    publicProfile: true, // Alias of visibility; exists to simplify reactivity of the visibility checkbox.
    role: 'listener',
    image_url: '',
})
const playlists = reactive([])

// Fetches and assigns user data reactive,
// as well as marking the page as loaded and storing error message, if any.
async function fetchUserData() {
    try {
        Object.assign(user, await UserService.get(getUsername()))
        user.publicProfile = user.visibility === 'public'

        user.image_url = user.image_url === null? AvatarSvg : user.image_url ;
        
        console.log(user.image_url)
        // Don't show private profiles unless they belong to the user.
        // TODO this should be done in the backend, but I felt like "mocking" it now
        // so we don't get embarrassed in the demo over a checkbox for a not-fully-implemented feature.
        // Arguably this checkbox should not have been planned for this sprint and should've been part of the US for profile visibility. 
        if (user.visibility === 'private' && getUsername() !== UserService.getCurrentUsername()) {
            errorMsg.value = 'The profile is private.'
        } else {
            // Clear any previous error message so the new profile is shown
            errorMsg.value = null
        }
    } catch (err) {
        errorMsg.value = (err.response) ? err.response.data.detail : err.message
    } finally {
        // Mark the page as loaded in either case
        isLoaded.value = true
    }
    try {
        // Fetch playlists
        Object.assign(playlists, await PlaylistService.getUserPlaylists(getUsername()))
    } catch (err) {
        Toast.fireError('Failed to load playlists')
    }
}

function getUsername() {
    return route.params.username
}

const isArtist = computed(() => {
    return user.role === 'artist'
})

function toggleEditMode() {
    // Post to save changes
    if (isEditing.value) {
        UserService.updateProfile({
            genre: user.genre,
            description: user.description,
            visibility: user.visibility,
        }).then(() => {
            Toast.fire({
                title: 'Profile updated',
                icon: 'success',
            })
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

async function fetchUserRole() {
    const username = UserService.getCurrentUsername();
    if (username) {
        try {
            userRole.value = await UserService.getUserRole(username); 
        } catch (error) {
            console.error("Error obteniendo el rol del usuario:", error);
            userRole.value = null; 
        }
    }
}

async function toggleFollow(){
    if(UserService.isLoggedIn()){
        if(isFollowing.value){
            try {
                await ListenerService.unfollow(getUsername());
                isFollowing.value = !isFollowing.value;
                Toast.fire({
                    title: 'Unfollow successful!',
                    icon: 'success',
                });
            } catch (error) {
                console.error("Error following:", error);
                Swal.fire({
                    title: 'Unfollow failed',
                    text: 'Reason: ' + err.response.data.detail,
                    icon: 'error',
                })
            }
        }
        else{
            try {
                await ListenerService.follow(getUsername());
                isFollowing.value = !isFollowing.value;
                Toast.fire({
                    title: 'Follow successful!',
                    icon: 'success',
                });
            } catch (error) {
                console.error("Error following:", error);
                Swal.fire({
                    title: 'Follow failed',
                    text: 'Reason: ' + err.response.data.detail,
                    icon: 'error',
                })
            }
        }
    }
    else{
        Toast.fire({
            title: 'You need to be logged in to send questions to artists',
            icon: 'warning',
            timer: 3000,
        });
        router.push('/');
    }
}

function deletePlaylist(id) {
    Swal.fire({
        title: "Delete playlist",
        text: "Are you sure you want to delete this playlist?",
        showCancelButton: true,
    }).then((response) => {
        if (response.isConfirmed) {
            PlaylistService.delete(id).then(() => {
                playlists.splice(playlists.findIndex((el) => el.playlist_id === id), 1)
            }).catch((err) => {
                Swal.fire({
                    title: 'Error',
                    text: 'Failed to delete playlist: ' + err,
                    icon: 'error',
                })
            })
        }
    })
}

function toggleVisibility() {
    // Clicking the badge outside of edit mode is no-op.
    if (isEditing.value) {
        user.visibility = user.visibility === 'private' ? 'public' : 'private'
        user.publicProfile = !user.publicProfile
    }
}

function deleteAccount() {
    Swal.fire({
        title: 'Are you sure?',
        text: "This action cannot be undone. You will lose access to EchoLink and your profile will be permanently deleted.",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#d33',
        cancelButtonColor: '#3085d6',
        confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
        if (result.isConfirmed) {
            UserService.deleteAccount()
                .then((response) => {
                    Cookies.remove('auth_token');
                    Cookies.remove('logged_in');
                    Swal.fire(
                        'Deleted!',
                        response.detail,
                        'success'
                    ).then(() => {
                        window.location.href = "/";
                    });
                })
                .catch((err) => {
                    Swal.fire({
                        title: 'Error',
                        text: 'Failed to delete account: ' + (err.response ? err.response.data.detail : err.message), icon: 'error',
                    });
                });
        }
    });
}

function askQuestion() {
    if(UserService.isLoggedIn() && isFollowing.value){
        Swal.fire({
            title: 'Ask me something!',
            html: `
            <div style="display: flex; flex-direction: column; align-items: center; width: 100%;">
                <textarea 
                    id="swal-input" 
                    class="swal2-textarea" 
                    maxlength="500" 
                    style="width: 100%; max-width: 500px; height: 100px; resize: none; padding: 10px; box-sizing: border-box;" 
                    placeholder="Type your question here..."></textarea>
                <div 
                    id="char-counter" 
                    style="width: 100%; max-width: 500px; text-align: right; font-size: 0.9em; color: #555; margin-top: 5px;">
                    0/500 characters
                </div>
            </div>
            `,
            showCancelButton: true,
            confirmButtonText: 'Send',
            cancelButtonText: 'Cancel',
            preConfirm: () => {
                const question = document.getElementById('swal-input').value;
                // Check text (can't be empty)
                if (!question || question.trim().length === 0) {
                    Swal.showValidationMessage('The question cannot be empty');
                    return false;
                } else {
                    return question;
                }
            },
            didOpen: () => {
                const input = document.getElementById('swal-input');
                const counter = document.getElementById('char-counter');

                input.addEventListener('input', () => {
                    const charCount = input.value.length;
                    counter.textContent = `${charCount}/500 characters`;
                });
            }
        }).then((result) => {
            if (result.isConfirmed && result.value) {
                QuestionService.newQuestion(getUsername(), result.value)
                    .then(() => {
                        Toast.fire({
                            title: 'Your question has been sent successfully!',
                            icon: 'success',
                        });
                    })
                    .catch((err) => {
                        Swal.fire({
                            title: 'Error',
                            text: 'Failed to send the question: ' + (err.response ? err.response.data.detail : err.message),
                            icon: 'error',
                        });
                    });
            }
        });
    }
    else if(UserService.isLoggedIn() && !isFollowing.value){
        Toast.fire({
            title: 'You need to follow the artist to send them questions',
            icon: 'warning',
            timer: 3000,
        });
    }
    else{
        Toast.fire({
            title: 'You need to be logged in to send questions to artists',
            icon: 'warning',
            timer: 3000,
        });
        router.push('/logIn');
    }
    
}

function goToPlaylistCreator(){
    router.push('/playlists/new');
}



const visiblePlaylists = computed(() => {
    // Only show private playlists for their creator
    // TODO this should be done by backend instead for security reasons
    return isOwnProfile.value ? playlists : playlists.filter((playlist) => playlist.visibility === 'public')
})

const isOwnProfile = computed(() => {
    return UserService.isLoggedIn() && UserService.getCurrentUsername() === getUsername()
})

const accountTypeBadgeTooltip = computed(() => {
    return isArtist.value ? 'This is an artist account.' : 'This is a personal account.'
})

const roleName = computed(() => {
    return isArtist.value ? 'Artist' : 'Music Fan'
})

const visibilityBadgeTooltip = computed(() => {
    return user.visibility === 'public' ? 'Any user can access your profile.' : 'Only you can see your profile.'
})

const editableFieldClass = computed(() => {
    return {
        "details-field-editable": isEditing.value,
    }
})

// Make the badge behave like a button when in edit mode,
// as clicking it will also interact with the checkbox.
const visibilityBadgeClass = computed(() => {
    return {
        "hover:bg-blue-600": isEditing.value,
        "focus:bg-blue-600": isEditing.value,
        "active:bg-blue-500": isEditing.value,
    }
})

// Refetch user data when navigating to another profile from this page (ex. directly rewriting the URL or using the header button)
// This is necessary as the component won't be recreated, thus onMounted() won't fire.
watch(
    () => route.params,
    async (newId) => {
        fetchUserData(newId)
        isFollowing.value = await ListenerService.checkFollow(getUsername())
        fetchUserRole();
    },
)

// Fetch user data when the page is accessed from another one.
onMounted(async function () {
    fetchUserData(getUsername())
    isFollowing.value = await ListenerService.checkFollow(getUsername())
    fetchUserRole();
})

</script>

<style scoped>

.page-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start; /* Align items to the top */
    min-height: 100vh; /* Ensure the container takes the full height of the viewport */
}

.btn {
    @apply font-bold py-3 px-4 rounded;
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
    padding: 20px; /* Esto puede ser ajustado si es necesario */
    min-width: 320px; /* Un ancho mínimo para la ventana emergente */
    max-width: 600px; /* Ancho máximo de la ventana emergente */
    width: 90%; /* Puedes ajustarlo según lo que prefieras */
}

@media (max-width: 900px) {
    .container-main {
        width: 90%; /* Full viewport width for small screens */
        height: auto; /* Full viewport height for small screens */
        margin-top: 10vh; /* Remove margin for full screen effect */
        border-radius: 0; /* Remove border radius for full screen effect */
    }
    

}
</style>