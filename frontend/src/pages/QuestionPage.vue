<template>
	<div>
		<div class="home-two-light my-app home-light page-container">

			<HeaderComponent />

			<div class="lg:px-4 mx-auto max-w-screen-xl">
				<h2>Your Questions</h2>
				<p>See if your artists answered you.</p>

				<!-- Search and Filters Container -->
				<div class="search-and-filters w-full flex flex-col gap-4">
					<!-- Search Bar -->
					<TextInput class="search-bar w-full" placeholder="Search by Artist or Question Content..."
						input-type="text" :value="search.text" @changed="search.text = $event"></TextInput>

					<!-- Dropdown Filters -->
					<div class="filters-container flex flex-col lg:flex-row gap-4 w-full">
						<!-- Filter By Dropdown -->
						<div class="dropdown w-full lg:w-1/2">
							<OptionSelector v-model="search.filter" :options="filters" label="Filter by" track-by="id"
								option-label-key="label" :allow-empty="false" :can-search="true"></OptionSelector>
						</div>

						<!-- Sort By Dropdown -->
						<div class="dropdown w-full lg:w-1/2">
							<OptionSelector v-model="search.order" :options="orders" label="Sort by" track-by="id"
								option-label-key="label" :allow-empty="false" :can-search="true"></OptionSelector>
						</div>
					</div>
				</div>

				<div class="mx-2 my-2" /> <!-- Spacing -->

				<!-- Questions Container -->
				<div v-if="!sortedQuestionsError && filterQuestions().length > 0"
					class="questions-container mx-auto mt-2">
					<QuestionCard v-for="question in filterQuestions()" :key="question.question_id" :question="question"
						@archived="onQuestionArchived(question)"></QuestionCard>
				</div>
				<p v-else-if="sortedQuestionsError" class="text-gray-500">Something went wrong while fetching latest
					questions:<br>{{ sortedQuestionsError }}.<br>Try refreshing the page.</p>
				<p v-else-if="sortedQuestions.length == 0" class="text-gray-500">You have made no questions to artists
					yet. Visit their profiles to start asking questions.</p>

				<p v-else class="text-gray-500"> No questions found using your filter!</p>
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
import QuestionCard from '../components/QuestionCard.vue';
import QuestionService from '../services/question.js';
import Swal from 'sweetalert2';
import Toast from '../utilities/toast.js'
import { reactive, ref, computed, onMounted, onBeforeUnmount, watch, onUpdated } from 'vue';

const search = reactive({
	filter: { id: 0, label: 'All' },
	text: '',
	order: { id: 0, label: 'Default' },
})
const orders = reactive([
	{ id: 0, label: 'Default' },
	{ id: 1, label: 'From New to Old' },
	{ id: 2, label: 'From Old to New' },
])

let fetchedQuestions = []
const sortedQuestions = reactive([])
const sortedQuestionsError = ref(null)
const filters = reactive([
	{ id: 0, label: 'All' },
	{ id: 1, label: 'Awaiting Response' },
	{ id: 2, label: 'Answered' },
	{ id: 3, label: 'Rejected' },
	{ id: 4, label: 'Archived' },
]);
const previousFilterId = ref(search.filter.id);


watch(() => search.filter.id, (newValue) => {
	if (previousFilterId.value !== newValue) {
		previousFilterId.value = newValue;
	}
})


function filterQuestions() {

	let filtered = [...sortedQuestions];

	if (search.filter.id !== 0) {
		const statusMap = {
			1: 'waiting',
			2: 'answered',
			3: 'rejected',
			4: 'archived',
		};

		if (search.filter.id === 4) {
			// Special case for archived
			filtered = filtered.filter(question => question.archived === true);
		} else {
			// Filter by status
			filtered = filtered.filter(question => question.response_status === statusMap[search.filter.id]);
		}
	}

	// Apply search text filter 
	if (search.text.trim() !== '') {
		const searchText = search.text.toLowerCase();
		filtered = filtered.filter(question =>
			question.artist_username.toLowerCase().includes(searchText) ||
			question.question_text.toLowerCase().includes(searchText) // Search in artist name
		);
	}

	// Sort the filtered questions based on the selected order
	if (search.order.id === 1) {
		// From New to Old
		filtered.sort((a, b) => new Date(b.question_date) - new Date(a.question_date));
	} else if (search.order.id === 2) {
		// From Old to New
		filtered.sort((a, b) => new Date(a.question_date) - new Date(b.question_date));
	}

	return filtered;
}


async function fetchQuestions() {
	console.log("Questions loaded: ")
	try {
		fetchedQuestions = await QuestionService.getQuestions()
		Object.assign(sortedQuestions, fetchedQuestions)
		console.log(sortedQuestions.length)
		for (const question of sortedQuestions) {
			console.log(question)
		}

	} catch (err) {
		sortedQuestionsError.value = (err.response) ? err.response.data.detail : err.message
	}
}

onUpdated(() => {
	updateProgress() // Must update the scroll widget as the page dimensions most likely changed, ex. if songs were fetched.
})

function scrollToTop() {
	window.scrollTo({ top: 0, behavior: 'smooth' });
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

const updateProgress = () => {
	const progressPath = document.querySelector(".progress-wrap path");
	const pathLength = 307.919;
	const scrollTop = window.scrollY;
	const docHeight = document.documentElement.scrollHeight - window.innerHeight;
	const progress = (scrollTop / docHeight) * 100;

	const offset = pathLength - (pathLength * progress) / 100;
	progressPath.style.strokeDashoffset = offset;
};

onMounted(() => {
	fetchQuestions();

	window.addEventListener("scroll", updateProgress);
	updateProgress();
})

onBeforeUnmount(() => {
	window.removeEventListener("scroll", updateProgress);
});

</script>

<style scoped>
/* Page container styles */
.page-container {
    width: 100vw;
    max-width: 100%;
    padding: 0 10px; /* Adjust padding for smaller screens */
    margin: 0 auto;
}

/* Questions Container */
.questions-container {
    width: 100%;
    margin: 0 auto;
}

/* Add margin between question cards */
.questions-container > * {
    margin: 10px; /* Adjust the value as needed */
}

/* Search and Filter adjustments */
.search-and-filters {
    width: 100%;
    padding: 0;
}

.dropdown {
    width: 100%;
}

/* Question cards grid layout */
@media (min-width: 768px) {
    .questions-container {
        grid-template-columns: repeat(2, 1fr);
    }
}

@media (min-width: 1024px) {
    .questions-container {
        grid-template-columns: repeat(3, 1fr);
    }
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