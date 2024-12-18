<template>
	<div v-if="!isLoggedIn()">
		<div class="home-two-light my-app home-light container">
			<Header />
			<Banner />
			<Broadcast />

			<!-- Explore Section -->
			<div class="explore-section">
				<div class="explore-column">
					<a href="/artist" class="btn btn--primary">Explore all artists</a>
				</div>
				<div class="explore-column">
					<a href="/music" class="btn btn--primary">Explore songs</a>
				</div>
			</div>

			<Footer class="footer-light mx-10" />
		</div>
		<div class="progress-wrap active-progress" @click="scrollToTop">
			<svg width="100%" height="100%" viewBox="-1 -1 102 102" class="progress-circle svg-content">
				<path d="M50,1 a49,49 0 0,1 0,98 a49,49 0 0,1 0,-98" style="transition: stroke-dashoffset 10ms linear; stroke-dasharray: 307.919, 307.919; stroke-dashoffset: 178,377;"></path>
			</svg>
		</div>
	</div>
	<!-- Show dashboard instead if the user is logged in -->
	<div v-else>
		<ListenerDashboard />
	</div>
</template>

<script>
import Header from '../components/HeaderComponent.vue';
import Footer from '../components/FooterComponent.vue';
import Banner from '../components/BannerComponent.vue';
import Broadcast from '../components/BroadcastComponent.vue';
import ListenerDashboard from '../pages/ListenerDashboard.vue';
import UserService from '../services/user.js';

export default {
	name: "HomeLight",
	components: {
		Header,
		Footer,
		Banner,
		Broadcast,
		ListenerDashboard,
	},
	mounted() {
		if (!this.isLoggedIn()) {
			const progressPath = this.$el.querySelector(".progress-wrap path");
			const pathLength = 307.919;

			const updateProgress = () => {
				const scrollTop = window.scrollY;
				const docHeight = document.documentElement.scrollHeight - window.innerHeight;
				const progress = (scrollTop / docHeight) * 100;

				const offset = pathLength - (pathLength * progress) / 100;
				progressPath.style.strokeDashoffset = offset;
			};

			window.addEventListener("scroll", updateProgress);
			updateProgress();
		}
	},
	beforeDestroy() {
		window.removeEventListener("scroll", this.updateProgress);
	},
	methods: {
		scrollToTop() {
			window.scrollTo({ top: 0, behavior: 'smooth' });
		},
		isLoggedIn() {
			return UserService.isLoggedIn();
		},
	},
};
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

.footer-light {
	width: 100vw;
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