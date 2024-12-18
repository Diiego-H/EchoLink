<template>
	<div>
		<div class="home-two-light my-app home-light page-container relative">

			<HeaderComponent />

			<div class="lg:px-4 mx-auto max-w-screen-xl">
				<h2>Explore Songs</h2>
				<p>Discover new songs of artists</p>

				<!-- Search and Filters Container -->
				<div class="search-and-filters w-full flex flex-col gap-4">
					<!-- Search Bar -->
					<TextInput
						class="search-bar w-full"
						placeholder="Search by name or artist..."
						input-type="text"
						:value="search.text"
						@changed="search.text = $event"
					></TextInput>

					<!-- Dropdown Filters -->
					<div class="filters-container flex flex-col lg:flex-row gap-4 w-full">
						<!-- Genre Dropdown -->
						<div class="dropdown w-full lg:w-1/2">
							<OptionSelector
								v-model="search.genre"
								:options="genres"
								label="Genre"
								track-by="id"
								option-label-key="label"
								:allow-empty="false"
								:can-search="true"
							></OptionSelector>
						</div>

						<!-- Sort Dropdown -->
						<div class="dropdown w-full lg:w-1/2">
							<OptionSelector
								v-model="search.filter"
								:options="filters"
								label="Sort"
								track-by="id"
								option-label-key="label"
								:allow-empty="false"
								:can-search="true"
							></OptionSelector>
						</div>
					</div>
				</div>

				<div class="mx-2 my-2" /> <!-- Spacing -->

				<!-- Song Grid -->
				<div v-if="sortedSongsError === null" class="flex flex-col items-center mt-3 gap-4">
					<div class="song-grid">
						<p v-if="sortedSongs.length === 0" class="text-gray-500 w-100">
							There are no songs that match your search criteria.
						</p>
						<div class="grid-container">
							<SongItem
								v-for="(song, index) in validSongs"
								:key="index"
								:song="song"
								class="song-item"
							/>
						</div>
					</div>
				</div>
				<p v-else class="text-gray-500">
					Something went wrong while fetching latest songs:<br />
					{{ songsError }}.<br />
					Try refreshing the page.
				</p>
			</div>

			<FooterComponent class="footer-light mx-10" />
		</div>
		<div class="progress-wrap active-progress" @click="scrollToTop">
			<svg width="100%" height="100%" viewBox="-1 -1 102 102" class="progress-circle svg-content">
				<path
					d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98"
					style="transition: stroke-dashoffset 10ms linear; stroke-dasharray: 307.919, 307.919; stroke-dashoffset: 178,377;"
				></path>
			</svg>
		</div>
	</div>
</template>

<script setup>
import HeaderComponent from '../components/HeaderComponent.vue';
import FooterComponent from '../components/FooterComponent.vue';
import TextInput from '../components/form/TextInput.vue';
import OptionSelector from '../components/form/OptionSelector.vue';
import SongItem from '../components/SongItem.vue'; // Use SongItem instead of SongList
import SongService from '../services/song.js';
import { reactive, ref, computed, onMounted, onBeforeUnmount, watch, onUpdated } from 'vue';

const search = reactive({
	genre: { id: 'all', label: 'All' },
	text: '',
	filter: { id: 1, label: 'Alphabetically' },
});
const genres = reactive([]);
const registeredGenres = ref(new Set());
const songsError = ref(null);
const sortedSongs = reactive([]);
const sortedSongsError = ref(null);
const filters = reactive([
	{ id: 1, label: 'Alphabetically' },
	{ id: 2, label: 'By release date' },
	{ id: 3, label: 'By artist engagement' },
	{ id: 4, label: 'By listener affinity' },
]);
const previousFilterId = ref(search.filter.id);

watch(
	() => search.filter.id,
	(newValue) => {
		if (previousFilterId.value !== newValue) {
			previousFilterId.value = newValue;
			fetchSongs();
		}
	}
);

async function fetchSongs() {
	try {
		let fetchedSongs;
		switch (search.filter.id) {
			case 1:
				fetchedSongs = await SongService.getSortedAlphabetically();
				break;
			case 2:
				fetchedSongs = await SongService.getSortedReleaseDate();
				break;
			case 3:
				fetchedSongs = await SongService.getSortedEngagement();
				break;
			case 4:
				fetchedSongs = await SongService.getSortedPriority();
				break;
		}
		for (const index in fetchedSongs) {
			const song = fetchedSongs[index];

			// Add an extra field to improve vue-multiselect search support (since it only supports searching by one key)
			song.fullTitle = `${song.artist_name} - ${song.title}`;

			// Track all used genres
			if (!registeredGenres.value.has(song.genre)) {
				const capitalizedGenre = song.genre
					.split(' ')
					.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
					.join(' ');
				genres.push({ id: song.genre, label: capitalizedGenre });
				registeredGenres.value.add(song.genre);
			}
		}

		if (!genres.some((genre) => genre.id === 'all')) {
			genres.unshift({ id: 'all', label: 'All' });
		}

		Object.assign(sortedSongs, fetchedSongs);
	} catch (err) {
		sortedSongsError.value = err.response ? err.response.data.detail : err.message;
	}
}

onUpdated(() => {
	updateProgress(); // Must update the scroll widget as the page dimensions most likely changed, ex. if songs were fetched.
});

function scrollToTop() {
	window.scrollTo({ top: 0, behavior: 'smooth' });
}

const validSongs = computed(() => {
	const searchText = search.text.toLowerCase(); // Convert search input to lowercase
	const results = sortedSongs.filter((song) => {
		const fullTitle = song.fullTitle.toLowerCase(); // Convert song title and artist to lowercase
		const genreMatch = search.genre === null || search.genre.id === song.genre || search.genre.id === 'all';
		const textMatch = search.text === '' || fullTitle.includes(searchText); // Perform case-insensitive search
		return textMatch && genreMatch;
	});
	return results;
});

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
	fetchSongs();

	window.addEventListener('scroll', updateProgress);
	updateProgress();
});

onBeforeUnmount(() => {
	window.removeEventListener('scroll', updateProgress);
});
</script>

<style scoped>
.page-container {
	width: 100vw;
	display: flex;
	flex-direction: column;
	align-items: center;
	justify-content: flex-start;
}

.song-grid {
	width: 100%;
	display: flex;
	flex-direction: column;
	align-items: center;
}

.grid-container {
	display: grid;
	grid-template-columns: repeat(1, 1fr); /* Default to 1 column */
	gap: 20px;
	width: 100%;
}

.song-item {
	width: 80vw; /* Default width for small screens */
	height: auto;
}

@media (min-width: 768px) {
	.grid-container {
		grid-template-columns: repeat(2, 1fr); /* 2 columns for medium and large screens */
	}
	.song-item {
		width: 40vw; /* Adjust width for larger screens */
	}
}
</style>