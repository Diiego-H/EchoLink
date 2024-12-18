<template>
	<div>
		<div class="home-two-light my-app home-light page-container relative">

			<HeaderComponent />

			<div class="lg:px-4 mx-auto max-w-screen-xl">
				<h2>Explore Artists</h2>
				<p>Discover and connect with fantastic musicians, artists, and creators – explore their world and get inspired!</p>
				<div class="search-and-filters w-full flex flex-col gap-4">
    <!-- Search Bar -->
    <TextInput
        class="search-bar w-full"
        placeholder="Search by Artist or Content..."
        input-type="text"
        :value="search.text"
        @changed="search.text = $event"
    ></TextInput>

    <!-- Dropdown Filters -->
    <div class="filters-container flex flex-col lg:flex-row gap-4 w-full">
        <OptionSelector
            class="dropdown w-full lg:w-1/2"
            v-model="search.genre"
            :options="genres"
            label="Filter by Genre"
            track-by="id"
            option-label-key="label"
            :allow-empty="false"
            :can-search="true"
        ></OptionSelector>

        <OptionSelector
            class="dropdown w-full lg:w-1/2"
            v-model="search.order"
            :options="orders"
            label="Sort by"
            track-by="id"
            option-label-key="label"
            :allow-empty="false"
            :can-search="true"
        ></OptionSelector>
    </div>
</div>

				<div class="mx-2 my-2" /> <!-- Spacing -->

				<!-- Loading Carousel -->
				<div v-if="isLoading" class="flex justify-center items-center mt-10">
					<LoadingSpinner />
				</div>

				<!-- Artist Grid -->
				<div v-else-if="!sortedArtistsError && filteredArtists.length > 0"
					class="flex-col items-center mt-3 gap-4">
					<div class="lg:flex-row items-center justify-center gap-4">
						<div class="artist-grid mt-4">
							<div v-for="artist in filteredArtists" :key="artist.username" class="artist-card">
								<ArtistComponent @edited="handleArtistEdited" :artist="artist" />
							</div>
						</div>
					</div>
				</div>

				<p v-else-if="sortedArtistsError" class="text-gray-500">Something went wrong while fetching latest
					artists: {{ sortedArtistsError }}. Try refreshing the page.</p>
				<p v-else-if="sortedArtists.length == 0" class="text-gray-500">There are no artists registered on the
					platform.</p>

				<p v-else class="text-gray-500">No artists matched your search criteria!</p>
			</div>

			<FooterComponent class="footer-light mx-10" />
		</div>
		<div class="progress-wrap active-progress" @click="scrollToTop">
			<svg width="100%" height="100%" viewBox="-1 -1 102 102" class="progress-circle svg-content">
				<path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98"
					style="transition: stroke-dashoffset 10ms linear; stroke-dasharray: 307.919, 307.919; stroke-dashoffset: 178,377;">
				</path>
			</svg>
		</div>

	</div>
</template>
<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import OptionSelector from '../components/form/OptionSelector.vue';
import ArtistComponent from '../components/ArtistComponent.vue';
import LoadingSpinner from '../components/LoadingSpinner.vue'; // Import the LoadingSpinner component
import ArtistService from '../services/artist.js'; // Assume this service handles API calls
import { reactive, ref, computed, onMounted, onBeforeUnmount, onUpdated } from 'vue';
import fixedImage from '../assets/images/cara1.jpg';
import ListenerService from '../services/listener.js';

const genres = reactive([{ id: 'all', label: 'All' }]);
const registeredGenres = ref(new Set());

const search = reactive({
	genre: { id: 'all', label: 'All' },
	text: '',
	order: { id: 0, label: 'Engagement' },
});

let fetchedArtists = [];
const sortedArtists = reactive([]);
const sortedArtistsError = ref(null);
const isLoading = ref(true); // Add a loading state
const orders = reactive([
	{ id: 0, label: 'Engagement' },
	{ id: 1, label: 'Followers' },
	{ id: 2, label: 'Alphabetically' },
]);
const filteredArtists = computed(() => {
	let filtered = [...sortedArtists];

	// Filter by genre
	if (search.genre.id !== 'all') {
		filtered = filtered.filter((artist) => artist.genre === search.genre.id);
	}

	// Filter by search text
	if (search.text.trim() !== '') {
		const searchText = search.text.toLowerCase();
		filtered = filtered.filter((artist) =>
			artist.username.toLowerCase().includes(searchText) ||
			artist.genre.toLowerCase().includes(searchText)
		);
	}


	if (search.order.id === 2) {
		// Alphabetical order
		filtered.sort((a, b) => a.username.localeCompare(b.username));

	} else if (search.order.id === 0) {
		// Followers
		filtered.sort((a, b) => a.rank_data.ranking - b.rank_data.ranking);
	}

	return filtered;
});



async function fetchArtists() {
	try {
		
		isLoading.value = true;
		fetchedArtists = await ArtistService.getArtistByFollowers();
		fetchedArtists = fetchedArtists.map((artist) => ({
			...artist,
			image: artist.image_url || fixedImage,
		}));

		for (const index in fetchedArtists) {
			const artist = fetchedArtists[index];

			if (!registeredGenres.value.has(artist.genre)) {
				const capitalizedGenre = artist.genre
					.split(' ')
					.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
					.join(' ');
				genres.push({ id: artist.genre, label: capitalizedGenre });
				registeredGenres.value.add(artist.genre);
			}
		}

		if (!genres.some((genre) => genre.id === 'all')) {
			genres.unshift({ id: 'all', label: 'All' });
		}
		console.log(fetchedArtists);
		Object.assign(sortedArtists, fetchedArtists);
	} catch (err) {
		sortedArtistsError.value = err.response ? err.response.data.detail : err.message;
	} finally {
		isLoading.value = false; // Set loading to false after fetching
	}
}


async function updateCanAsk(index, updatedArtist) {
	const artist = sortedArtists[index];
	try {
		// Fetch the updated can_ask status
		updatedArtist.can_ask = await ListenerService.canAsk(artist.username);

		// Update the sortedArtists array
		// If sortedArtists is a reactive property, Vue will automatically track changes
		sortedArtists[index] = { ...updatedArtist }; // Spread to ensure reactivity

		// Return the updated can_ask value
		return sortedArtists[index].can_ask;
	} catch (err) {
		console.error('Error fetching canAsk:', err);
		return false;
	}
}


function handleArtistEdited(updatedArtist) {
	// Find the artist in the sortedArtists list
	const index = sortedArtists.findIndex((artist) => artist.username === updatedArtist.username);

	if (index !== -1) {
		// Update the artist's data in the list
		const artist = sortedArtists[index];

		// Check if `is_following` changed from false to true
		if (!artist.is_following && updatedArtist.is_following) {
			updateCanAsk(index, updatedArtist)
		}

		if (!updatedArtist.is_following) {
			updatedArtist.can_ask = false;
		}


		// Update the artist in the list
		sortedArtists[index] = updatedArtist;
	}
}

onUpdated(() => {
	updateProgress(); // Must update the scroll widget as the page dimensions most likely changed, ex. if artists were fetched.
});

function scrollToTop() {
	window.scrollTo({ top: 0, behavior: 'smooth' });
}

const updateProgress = () => {
	const progressPath = document.querySelector('.progress-wrap path');
	const pathLength = 307.919;
	const scrollTop = window.scrollY;
	const docHeight = document.documentElement.scrollHeight - window.innerHeight;
	const progress = (scrollTop / docHeight) * 100;

	const offset = pathLength - (pathLength * progress) / 100;
	progressPath.style.strokeDashoffset = offset;
};

onMounted(() => {
	fetchArtists();

	window.addEventListener('scroll', updateProgress);
	updateProgress();
});

onBeforeUnmount(() => {
	window.removeEventListener('scroll', updateProgress);
});
</script>
<style scoped>
.artist-card {
    position: relative;
    height: calc(90vw); /* 1/4th of the screen width */
    width: calc(90vw); /* 1/4th of the screen width */
    margin: 0 30px;
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

.view-all-artists-div {
	display: flex;
	flex-direction: column;
	justify-content: center;
	align-items: center;
}

.artist-grid {
	display: grid;
	grid-template-columns: repeat(1, 1fr);
	/* Default to 1 column */
	gap: 20px;
	/* Add spacing between grid items */
}

@media (min-width: 768px) {

	/* Medium screens (e.g., tablets) */
	.artist-grid {
		grid-template-columns: repeat(2, 1fr);
		/* 2 columns */
	}

	.artist-card {
    position: relative;
    height: calc(40vw); /* 1/4th of the screen width */
    width: calc(40vw); /* 1/4th of the screen width */
    margin: 0 30px;
}
}

@media (min-width: 1024px) {

	/* Large screens (e.g., desktops) */
	.artist-grid {
		grid-template-columns: repeat(3, 1fr);
		/* 3 columns */
	}

	.artist-card {
    position: relative;
    height: calc(22vw); /* 1/4th of the screen width */
    width: calc(22vw); /* 1/4th of the screen width */
    margin: 0 30px;
}
}

.home-two-light {
	position: relative;
	/* Ensure stacking context */
}

.artist-card {
	position: relative;
	z-index: 0;
	/* Ensure cards stay below header and selectors */
}

.header-component,
.footer-component {
	position: relative;
	z-index: 50;
	/* Ensure header and footer stay on top */
}

.content-block {
	position: relative;
	z-index: 10;
	/* Ensure selectors and search bar stay above other content */
}

.page-container {
	width: 100vw;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-start;
	/* Align items to the top */
}

@media (max-width: 768px) {
	/* Center the text at the top */
	h2, p {
		text-align: center;
		padding: 0 10px; /* Add some padding for better readability */
	}

	/* Center and resize the TextInput and OptionSelector */
	.search-and-filters {
		width: 100%; /* Ensure the container takes full width */
		display: flex;
		flex-direction: column; /* Stack the elements vertically */
		align-items: center; /* Center align the elements */
		gap: 10px; /* Add spacing between the elements */
	}

	.search-bar {
		width: 80%; /* Make the TextInput 80% of the screen width */
	}

	.filters-container {
		width: 80%; /* Make the dropdown container 80% of the screen width */
		flex-direction: column; /* Stack the dropdowns vertically */
		align-items: center; /* Center align the dropdowns */
		gap: 10px; /* Add spacing between the dropdowns */
	}

	.dropdown {
		width: 100%; /* Ensure dropdowns take full width of their container */
	}
}
</style>
