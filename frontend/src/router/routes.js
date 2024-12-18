

import HomeDef from '../pages/HomeDef.vue'
import RegisterDef from '../pages/RegisterDef.vue'
import ProfileDef from '../pages/ProfileDef.vue'
import LogInDef from '../pages/LogInDef.vue';
import PlaylistCreator from '../pages/PlaylistCreator.vue';
import UploadTrack from '../pages/UploadTrack.vue';
import UserService from '../services/user.js';
import ArtistDashboard from '../pages/ArtistDashboard.vue';
import SongDetails from '../pages/SongDetails.vue';
import QuestionPage from '../pages/QuestionPage.vue';
import ExploreSongs from '../pages/ExploreSongs.vue';
import ArtistPage from '../pages/ArtistPage.vue';


export default  [
        {
            path: '/',
            name: 'Home',
            component: HomeDef,
        },
        {
            path: '/register',
            name: 'Resgister',
            component: RegisterDef,
        },
        {
            path: '/login',
            name: 'LogIn',
            component: LogInDef,
        },
        {
            path: '/users/:username',
            name: 'User Profile',
            component: ProfileDef,
        },
        {
            path: '/playlists/:id',
            name: 'Playlist',
            component: PlaylistCreator,
        },
        {
            path: '/songs/:id',
            name: 'Song',
            component: SongDetails,
        },
        {
            path: '/music',
            name: 'Explore Songs',
            component: ExploreSongs,
        },
        {
            path: '/artist',
            name: 'Artist Page',
            component: ArtistPage,
        },
        {
            path: '/dashboard/',
            name: 'Artist Dashboard',
            component: ArtistDashboard,
            beforeEnter: async (to, from, next) => {
                try {
                    if (!UserService.isLoggedIn()) {
                        // Redirect to login page if no user is authenticated
                        next('/login');
                        return;
                    }
        
                    const role = await UserService.getUserRole(UserService.getCurrentUsername()); 
                    if (role === 'artist') {
                        next(); 
                    } else {
                        next('/'); // Redirect to the homepage if the user is not an artist
                    }
                } catch {
                    next('/'); // Redirect to the homepage in case of an error
                }
            },
        },
        {
            path: '/uploadTrack',
            name: 'UploadTrack',
            component: UploadTrack,
            beforeEnter: async (to, from, next) => {
                try {
                    const username = UserService.getCurrentUsername();
                    if (!username) {
                        // Redirect to login page if no user is authenticated
                        next('/login');
                        return;
                    }
        
                    const role = await UserService.getUserRole(username); 
                    if (role === 'artist') {
                        next(); 
                    } else {
                        next('/'); // Redirect to the homepage if the user is not an artist
                    }
                } catch (error) {
                    console.error('Error comprobando el rol del usuario:', error);
                    next('/'); // Redirect to the homepage in case of an error
                }
            },
        }, 
        {
            path: '/questions',
            name: 'QuestionPage',
            component: QuestionPage,
            beforeEnter: async (to, from, next) => {
                try {
                    if (!UserService.isLoggedIn()) {
                        // Redirect to login page if no user is authenticated
                        next('/login');
                        return;
                    }
        
                    const role = await UserService.getUserRole(UserService.getCurrentUsername()); 
                    if (role === 'listener') {
                        next(); 
                    } else {
                        next('/'); // Redirect to the homepage if the user is not an artist
                    }
                } catch {
                    next('/'); // Redirect to the homepage in case of an error
                }
            },
        },
    ];
