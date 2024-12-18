<template>
	<header :class="{ 'header-active': scrollPosition >= 100, }" class="header">
		<div class="container">
			<div class="row">
				<div class="col-lg-12">
					<nav class="nav">
						<div class="nav__content">
							<div class="nav__logo">
								<router-link to="/" @click="scrollToTop">
									<img :src="LogoURL" alt="Logo" style="max-width: 55px;" />
									<p class="font-bold text-3xl ml-3">EchoLink</p>
								</router-link>
							</div>
							<div class="nav__menu">
								<div class="nav__menu-logo d-flex d-xl-none">
									<router-link to="/" class="text-center hide-nav">
										<img :src="LogoURL" alt="Logo" />
										<p class="font-bold text-3xl ml-3">EchoLink</p>
									</router-link>
									<button aria-label="close the menu" class="nav__menu-close">
										<i class="fa-solid fa-xmark"></i>
									</button>
								</div>
								<ul class="nav__menu-items">

									<li class="nav__menu-item">
										<router-link to="/" class="nav__menu-link hide-nav">Home</router-link>
									</li>

									<li class="nav__menu-item nav__menu-item--dropdown">
										<a href="javascript:void(0)" class="nav__menu-link nav__menu-link--dropdown">
											Explore
										</a>
										<ul class="nav__dropdown">
											<li>
												<router-link to="/artist"
													class="nav__dropdown-item hide-nav">Artists</router-link>
											</li>
											<li>
												<router-link to="/music"
													class="nav__dropdown-item hide-nav">Music</router-link>
											</li>
											<li v-if="isLoggedIn && !isArtist()">
												<router-link to="/questions"
													class="nav__dropdown-item hide-nav">Questions</router-link>
											</li>
											
										</ul>
									</li>
							
									<!-- Must exist during onMount for all the event listeners to be registered properly; cannot be v-if'd. -->
									<li class="nav__menu-item nav__menu-item--dropdown" :style="!isArtist() || !isLoggedIn  ? {'display': 'none'} : {}" :data-test="'artist-menu'" >
										<a href="javascript:void(0)" class="nav__menu-link nav__menu-link--dropdown text-nowrap">
											Artist Management
										</a>
										<ul class="nav__dropdown">
											<li>
												<router-link to="/dashboard" :data-test="'artist-dashboard'" 
													class="nav__dropdown-item hide-nav">Dashboard</router-link>
											</li>
											<li>
												<router-link to="/uploadTrack" :data-test="'upload-track-laptop'"
													class="nav__dropdown-item hide-nav">Upload Track</router-link>
											</li>


										</ul>
									</li>
						

									<li v-if="!isLoggedIn" class="nav__menu-item d-block d-md-none">
										<router-link to="/logIn" :data-test="'login-mobile'" class="btn btn--secondary mb-4">
											Log In
										</router-link>
										<router-link to="/register" class="btn btn--secondary">
											Register
										</router-link>
									</li>
									<li v-else class="nav__menu-item d-block d-md-none">
										<button @click="goToProfile" data-test="profile-mobile"class="btn btn--secondary mb-4">
											My Profile
										</button>
										<button @click="logout_function" :data-test="'logout-mobile'" class="btn btn--secondary"
											data-test="button-logout">
											Log Out
										</button>
									</li>
								</ul>
							</div>
							<div class="nav__uncollapsed">
								<div class="nav__uncollapsed-item d-none d-md-flex">
									<router-link v-if="!isLoggedIn" :data-test="'login-laptop'" to="/logIn" class="btn btn--secondary">
										Log In
									</router-link>
									<router-link v-if="!isLoggedIn" to="/register" class="btn btn--secondary">
										Register
									</router-link>
									<button v-if="isLoggedIn" :data-test="'profile-laptop'" @click="goToProfile" class="btn btn--secondary text-nowrap">
										My Profile
									</button>
									<button v-if="isLoggedIn" :data-test="'logout-laptop'" @click="logout_function" class="btn btn--secondary text-nowrap"
										data-test="button-logout">
										Log Out
									</button>
								</div>
								<button class="nav__bar d-block d-xl-none">
									<span class="icon-bar top-bar"></span>
									<span class="icon-bar middle-bar"></span>
									<span class="icon-bar bottom-bar"></span>
								</button>
							</div>
						</div>
					</nav>
				</div>
			</div>
		</div>
		<div class="backdrop"></div>
	</header>
</template>

<script>
import { ref } from 'vue';
import logo from '../assets/logo.png';
import UserService from '../services/user.js'
import Cookies from 'js-cookie';
import Swal from 'sweetalert2'

export default {
	name: "HeaderComponent",
	data: function () {
		return {
			scrollPosition: null,
			LogoSrc: logo,
			isLoggedIn: ref(Boolean(Cookies.get('logged_in'))),
			Toast: Swal.mixin({
				toast: true,
				position: 'top',
				iconColor: 'white',
				customClass: {
					popup: 'colored-toast',
				},
				showConfirmButton: false,
				timer: 1500,
				timerProgressBar: false,
			}),
			userRole: null,
		};
	},
	methods: {


		updateScroll() {
			this.scrollPosition =
				window.scrollY;
		},

		scrollToTop(){
			window.scrollTo({ top: 0, behavior: 'smooth' });
		},
		/*logout_function() {
			Cookies.remove('auth_token');
			Cookies.remove('logged_in');
			this.$router.push('/');
			this.isLoggedIn = false;
		},*/
		async logout_function() {
			try {
				await UserService.logout();

				Cookies.remove('auth_token');
				Cookies.remove('logged_in');

				this.$router.push('/logIn');

				this.isLoggedIn = false;

				this.Toast.fire({
					title: 'Log out successful!',
					icon: 'success',
				});

			} catch (error) {
				console.error('Error al cerrar sesión:', error);
				Cookies.remove('auth_token');
				Cookies.remove('logged_in');
				this.$router.push('/logIn');
			}
		},
		goToProfile() {
			const username = UserService.getCurrentUsername()
			// Sanity check.
			if (username !== null) {
				this.$router.push('/users/' + username)
			}
		},
		goToDashboard() {
			this.$router.push('/dashboard')
		},
		goToUploadTrack() {
			const username = UserService.getCurrentUsername()
			// Sanity check.
			if (username !== null) {
				this.$router.push('/uploadTrack')
			}
		},
		async fetchUserRole() {
			const username = UserService.getCurrentUsername();
			if (username) {
				try {
					this.userRole = await UserService.getUserRole(username); 
				} catch (error) {
					console.error("Error obteniendo el rol del usuario:", error);
					this.userRole = null; 
				}
			}
		},
		isArtist() {
			return this.userRole === "artist";
		},
	},
	mounted() {
		this.fetchUserRole();
		// Router won't exist in tests
		if (this.$router) {
			this.$router.beforeEach((to, from, next) => {
				window.scrollTo(0, 0);
				next();
			});
		}

		const navBars = document.querySelectorAll('.nav__bar');
		const navMenus = document.querySelectorAll('.nav__menu');
		const backdrops = document.querySelectorAll('.backdrop');
		const navDropdowns = document.querySelectorAll('.nav__dropdown');
		const navDropdownLinks = document.querySelectorAll('.nav__menu-link--dropdown');
		const navMenuClose = document.querySelectorAll('.nav__menu-close');
		const ticketModals = document.querySelectorAll('.ticket-modal');
		const conferenceModals = document.querySelectorAll('.conference-modal');
		const body = document.body;

		function toggleMenuActive() {
			navBars.forEach(navBar =>
				navBar.classList.toggle('nav__bar-toggle')
			);

			navMenus.forEach(navMenu =>
				navMenu.classList.toggle('nav__menu-active')
			);

			backdrops.forEach(backdrop =>
				backdrop.classList.toggle('backdrop-active')
			);

			//body.classList.toggle('body-active');
		}

		navBars.forEach(navBar => {
			navBar.addEventListener('click', function () {
				toggleMenuActive();
			});
		});

		backdrops.forEach(backdrop => {
			backdrop.addEventListener('click', function () {
				toggleMenuActive();
			});
		});

		navMenuClose.forEach(menuClose => {
			menuClose.addEventListener('click', function () {
				toggleMenuActive();
			});
		});

		window.addEventListener('resize', function () {
			backdrops.forEach(backdrop =>
				backdrop.classList.remove('backdrop-active')
			);

			navBars.forEach(navBar =>
				navBar.classList.remove('nav__bar-toggle')
			);

			navMenus.forEach(navMenu =>
				navMenu.classList.remove('nav__menu-active')
			);

			navDropdowns.forEach(navDropdown =>
				navDropdown.classList.remove('nav__dropdown-active')
			);

			navDropdownLinks.forEach(navDropdownLink =>
				navDropdownLink.classList.remove('nav__menu-link--dropdown-active')
			);

			body.classList.remove('body-active');

			ticketModals.forEach(ticketModal =>
				ticketModal.style.display = 'none'
			);

			conferenceModals.forEach(conferenceModal =>
				conferenceModal.style.display = 'none'
			);
		});

		navDropdownLinks.forEach(dropdownLink => {
			dropdownLink.addEventListener('click', function () {
				const dropdown = this.nextElementSibling;
				dropdown.classList.toggle('nav__dropdown-active');
				this.classList.toggle('nav__menu-link--dropdown-active');
			});
		});

	},
	props: {
		LogoSrc: {
			type: String,
			required: true,
		}
	},
	computed: {
		LogoURL() {
			return this.LogoSrc;
		},
	}, watch: {
		isLoggedIn(newValue, oldValue) {
			if (newValue !== oldValue) {
				this.isLoggedIn = Boolean(Cookies.get('logged_in'));
			}
		}
	},
};
</script>