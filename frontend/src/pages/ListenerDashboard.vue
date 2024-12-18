<template>
    <div class="home-two-light home-light container">
        <HeaderComponent />
        <div class="mx-auto w-100">
            <div class="banner content-block mx-auto w-100 mt-8 mb-4">
                <!-- Inner banner area -->
                <div class="sm:flex min-h-32 relative">
                    <!-- Avatar and username -->
                    <div class="flex items-center mx-auto">
                        <img class="max-w-32 min-w-20 h-auto rounded-3 border-black"
                            src="../assets/images/avatar.svg" />

                        <!-- TODO ensure contrast vs banner -->
                        <div class="flex flex-col items-start ms-3">
                            <p class="font-bold text-lg text-white">Welcome back, {{ getUsername() }}</p>
                            <p class="text-md text-white">See what's new on EchoLink.</p>
                        </div>
                    </div>
                </div>
            </div>

            

            <!-- Latest tracks -->

            <div class="explore-section" v-if="!isListener()">
				<div class="explore-column">
					<a href="/dashboard" class="btn btn--primary ">Go to your dashboard</a>
				</div>
				<div class="explore-column">
					<a href="/uploadTrack" class="btn btn--primary ">Upload a track</a>
				</div>
			</div>


            <div class="px-4 mx-auto" v-if="!isListener()">
                <hr class="h-divider my-5" />
                <h2>Explore tracks</h2>
                <p>Be the first to hear what's new on EchoLink, or find new tracks from your favourite genres.</p>

                <div v-if="songsError === null" class="flex flex-col-reverse lg:flex-row place-content-center w-100 mt-3">
                    <!-- Song list -->
                    <div class="flex flex-col flex-grow max-w-xl">
                        <p v-if="shownSongs.length === 0" class="text-gray-500 w-100">There are no songs that match your search criteria.</p>
                        <SongList class="flex-grow" v-model="shownSongs" :editable=false />
                    </div>

                    <div class="mx-2 my-2"/> <!-- Spacing -->

                    <!-- Search and filters -->
                    <div class="content-block max-h-min max-w-lg lg:min-w-96">
                        <p class="section-header mb-2">Filter</p>
                        
                        <TextInput label="Search" placeholder="Search by name or artist..." input-type="text" :value="search.text" @changed="search.text = $event"></TextInput>

                        <OptionSelector v-model="search.genre" :options="genres" label="Genre" track-by="id" option-label-key="label" :allow-empty="true" :can-search="true"></OptionSelector>
                    </div>
                </div>
                <p v-else class="text-gray-500">Something went wrong while fetching latest songs:<br>{{ songsError }}.<br>Try refreshing the page.</p>
                <button @click="router.push('/music')" class="btn btn--primary mt-3 min-w-64">
                            Explore all songs
                        </button>
            
            </div>

            <!-- Browse artists -->
            <div class="mx-auto" v-if="isListener()">
                <h2>Your artists</h2>
                <p>Connect with your favorite musicians on EchoLink by asking them questions and staying up to date with
                    their latest releases.</p>

                <ArtistsCarousel />

                <button @click="router.push('/artist')" class="btn btn--primary mt-3 min-w-64 text-black">
                    Explore all artists
                </button>
            </div>

            <!-- Songs -->
            <div v-if="isListener()" class="mx-auto">
                <hr class="h-divider my-5" />
                <h2>Your songs</h2>
                <p>This list of songs may be of your interest!</p>
                <div v-if="recommendationSongsError === null"
                    class="flex flex-col items-center w-100 mt-3 gap-x-4 h-full">
                    <template v-if="recommendationSongs.length > 0">
                        <div :class="{
                            'flex flex-col items-center': recommendationSongs.length <= 5,
                            'flex flex-col-reverse lg:flex-row items-center justify-center': recommendationSongs.length > 5
                        }" class="gap-x-4 w-full">
                            <div v-if="recommendationSongs.length <= 5" class="flex flex-col flex-grow max-w-xl">
                                <div v-for="song in recommendationSongs" :key="song.id" class="song-item">
                                    <SongList :value="[song]" :editable="false" />
                                </div>
                            </div>
                            <template v-else>
                                <div class="flex flex-col flex-grow max-w-xl">
                                    <div v-for="song in recommendationSongs.slice(0, Math.ceil(recommendationSongs.length / 2))"
                                        :key="song.id" class="song-item">
                                        <SongList :value="[song]" :editable="false" />
                                    </div>
                                </div>
                                <div class="flex flex-col flex-grow max-w-xl">
                                    <div v-for="song in recommendationSongs.slice(Math.ceil(recommendationSongs.length / 2))"
                                        :key="song.id" class="song-item">
                                        <SongList :value="[song]" :editable="false" />
                                    </div>
                                </div>
                            </template>
                        </div>

                        <button @click="router.push('/music')" class="btn btn--primary mt-3 min-w-64 text-black">
                            Explore songs
                        </button>
                    </template>
                    <template v-else>
                        <p class="text-gray-500 text-center mt-4">No recommendations available. Please check back later!
                        </p>
                    </template>
                </div>
                <p v-else class="text-gray-500">
                    Something went wrong while fetching your recommendation songs:<br />
                    {{ recommendationSongsError }}.<br />
                    Try refreshing the page.
                </p>
            </div>
            <hr class="h-divider my-5" />

            <!-- Questions -->
            <div v-if="isListener()" class="mx-auto">
                <h2>Your questions</h2>
                <p>See how artists have responded to your questions.</p>
                <div v-if="!questionsError && topQuestions.length > 0"
                    class="flex flex-col gap-y-4 mx-auto mt-2 max-w-screen-lg">
                    <QuestionCard v-for="question in topQuestions" :question="question"
                        @archived="onQuestionArchived(question)">
                    </QuestionCard>
                </div>
                <p v-else-if="questionsError" class="text-gray-500">Something went wrong while fetching latest
                    questions:<br>{{
                    songsError }}.<br>Try refreshing the page.</p>
                <p v-else-if="topQuestions.length == 0" class="text-gray-500">You have made no questions to artists yet.
                    Visit their
                    profiles to start asking questions.</p>

                <button @click="router.push('/questions')" class="btn btn--primary mt-3 min-w-64 text-black">
                    View all questions
                </button>
            </div>
        </div>

        <FooterComponent class="footer-light mx-10" />
    </div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import { PlusIcon } from '@heroicons/vue/24/solid'
import OptionSelector from '../components/form/OptionSelector.vue';
import ArtistsCarousel from '../components/ArtistsCarousel.vue';
import SongList from '../components/SongList.vue';
import QuestionCard from '../components/QuestionCard.vue';
import UserService from '../services/user.js'
import SongService from '../services/song.js'
import Swal from 'sweetalert2'
import Toast from '../utilities/toast.js'
import QuestionService from '../services/question.js'
import { computed, ref, reactive, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import ArtistService from '../services/artist.js'

const router = useRouter()

const LATEST_SONGS_STEP = 5 // Amount of additional songs to display when clicking "Show more"

const user = reactive({})
const songs = reactive([])
const recommendationSongs = reactive([])
const songsError = ref(null)
const recommendationSongsError = ref(null)
const shownSongsAmount = ref(3) // Ref in case we decide to make it customizable.
const genres = reactive([])
const registeredGenres = ref(new Set())
const search = reactive({
    genre: null,
    text: '',
})

const topQuestions = reactive([])
const topQuestionsError = ref(null)

async function fetchSongs() {
    try {
        const fetchedSongs = await SongService.getAll()
        for (const index in fetchedSongs) {
            const song = fetchedSongs[index]

            // Add an extra field to improve vue-multiselect search support (since it only supports searching by one key)
            song.fullTitle = `${song.artist_name} - ${song.title}`

            // Track all used genres
            if (!registeredGenres.value.has(song.genre)) {

                const capitalizedGenre = song.genre
					.split(' ')
					.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
					.join(' ');
				genres.push({ id: song.genre, label: capitalizedGenre });
                registeredGenres.value.add(song.genre)
            }
        }
        Object.assign(songs, fetchedSongs)
    } catch (err) {
        songsError.value = (err.response) ? err.response.data.detail : err.message
    }
}

async function fetchRecommendationSongs() {
    try {
        const fetchedRecommendationSongs = await SongService.getRecommendation()
        for (const index in fetchedRecommendationSongs) {
            const song = fetchedRecommendationSongs[index]

            // Add an extra field to improve vue-multiselect search support (since it only supports searching by one key)
            song.fullTitle = `${song.artist_name} - ${song.title}`
        }
        Object.assign(recommendationSongs, fetchedRecommendationSongs)
    } catch (err) {
        recommendationSongsError.value = (err.response) ? err.response.data.detail : err.message
    }
}

async function fetchQuestions() {
    try {
        const fetchedQuestions = await QuestionService.getTopQuestions()
        Object.assign(topQuestions, fetchedQuestions)
    } catch (err) {
        topQuestionsError.value = (err.response) ? err.response.data.detail : err.message
    }
}

async function fetchUser() {
    try {
        const userData = await UserService.get(UserService.getCurrentUsername())
        Object.assign(user, userData)
    } catch {
        Toast.fireError('Failed to load user data')
    }
}

function showMoreSongs() {
    shownSongsAmount.value += LATEST_SONGS_STEP
}

function splitSongs() {
    // Dividir las canciones en dos columnas
    const midPoint = Math.ceil(this.recommendationSongs.length / 2);
    return [
        this.recommendationSongs.slice(0, midPoint),
        this.recommendationSongs.slice(midPoint)
    ];
}

const validSongs = computed(() => {
    const searchText = search.text.toLowerCase(); // Convert search input to lowercase
    const results = songs.filter((song) => {
        const fullTitle = song.fullTitle.toLowerCase(); // Convert song title and artist to lowercase
        const genreMatch = search.genre === null || search.genre.id === song.genre;
        const textMatch = search.text === '' || fullTitle.includes(searchText); // Perform case-insensitive search
        return textMatch && genreMatch;
    });
    return results;
});


const shownSongs = computed(() => {
    const results = validSongs.value.slice(0, 5)
    return results
})

function getUsername() {
    return UserService.getCurrentUsername()
}

function isListener() {
    return user.role === 'listener'
}

function onQuestionArchived(question) {
    QuestionService.archiveQuestion(question.question_id).then(() => {
        Toast.fireSuccess('Question archived')
        fetchQuestions()
    }).catch((err) => {
        Swal.fire({
            title: 'Error',
            text: 'Failed to archive question: ' + ((err.response !== undefined) ? err.response.data.detail : err.message),
            icon: 'error',
        })
    })
}

// Fetch data when the page is accessed.
onMounted(function () {
    fetchSongs()
    fetchQuestions()
    fetchUser()
    fetchRecommendationSongs()
    ArtistService.getArtistByFollowers().then((a) => {
        console.log("Artists loaded")
        console.log(a)
    }).catch((err) => {
        console.error("Error loading artists: " + err)
    })
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

.footer-light {
    width: 100vw;
}

.section-header {
    @apply text-left font-bold text-xl
}

.btn-blue {
    @apply font-bold py-3 px-4 rounded;
    @apply bg-blue-500 text-white;
    @apply text-nowrap mb-2
}

.btn-blue:hover,
.btn-blue:focus {
    @apply bg-blue-700;
}

.banner {
    background-image: url("../assets/images/broadcast-bg.png");
    @apply bg-cover
}


.grid-container {
    display: grid;
    grid-template-columns: repeat(1, 1fr);
    /* Default to 1 column */
    gap: 20px;
    width: 100%;
}

.song-item {
    width: 90vw;
    /* Default width for small screens */
    height: auto;
}

@media (min-width: 768px) {
    .grid-container {
        grid-template-columns: repeat(2, 1fr);
        /* 2 columns for medium and large screens */
    }

    .song-item {
        width: 40vw;
        /* Adjust width for larger screens */
    }
}


/* Explore Section Styles */
.explore-section {
	display: flex;
	flex-direction: row; /* Default: buttons side by side */
	justify-content: space-between;
	align-items: center;
	margin-top: 40px;
	width: 100%; /* Full width */
	gap: 20px; /* Add spacing between buttons */
}

.explore-column {
	width: 100%; /* Ensure buttons take full width */
	display: flex;
	justify-content: center; /* Center the button */
}

/* Button Styles */
.btn {
	display: inline-block;
	text-align: center;
	font-weight: bold;
	padding: 15px 30px; /* Default padding */
	border-radius: 50px; /* Fully rounded corners */
	background-color: #3b82f6; /* Primary blue color */
	color: white;
	font-size: 16px; /* Default font size */
	text-decoration: none; /* Remove underline */
	cursor: pointer;
	transition: background-color 0.3s ease, transform 0.3s ease;
}

.btn--primary {
	background-color: #3b82f6; /* Primary blue */
}

.btn--primary:hover {
	background-color: #2563eb; /* Slightly darker blue on hover */
}

/* Bigger Buttons and Adjustments for Large Screens */
@media (min-width: 1024px) {
	.btn {
		padding: 20px 50px; /* Bigger padding for larger screens */
		font-size: 20px; /* Larger font size */
	}
}

/* Responsive Design for Small Screens */
@media (max-width: 768px) {
	.explore-section {
		flex-direction: column; /* Stack buttons vertically */
	}

	.btn {
		width: 100%; /* Buttons take full width on small screens */
	}
}
</style>