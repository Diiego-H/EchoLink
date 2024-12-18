import axios from './baseAxiosClient';
import Cookies from 'js-cookie'

class UserService {
    async registerAccount(username, email, password, role) {
        try {
            const response = await axios.post('/users/user', {
                'username': username,
                'email': email,
                'password': password,
                'role': role,
            });
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async loginAccount(email, password) {
        try{
            const response = await axios.post('/login', {
                'email': email,
                'password': password,
            });
            const data = response.data;
            const token = data.access_token;
            const username = data.username;

            if (!token) {
                throw new Error('Token not found in the response.');
            }

            Cookies.set('auth_token', token, {expires: 7});
            Cookies.set('username', username, {expires: 7});
            Cookies.set('logged_in', 'true', {expires: 7}) // Expire login flag after 7 days

            return response;
        } catch (error) {
            throw error;
        }
    }
    async logout() {
        try {
            const response = await axios.post('/login/logout', {}, this.getConfig());
            return response.data; 
        } catch (error) {
            throw error;
        }
    }
    async updateProfile(data) {
        try {
            const response = await axios.put('/users/user', data, this.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async get(username) {
        try {
            const response = await axios.get('/users/' + username);
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    isLoggedIn() {
        return (Cookies.get('auth_token') !== undefined) && (Cookies.get('username') !== undefined) // Checks both cookies for coherency.
    }
    // Returns the username of the current session,
    // or null if the client is not logged in.
    getCurrentUsername() {
        return this.isLoggedIn() ? Cookies.get('username') : null // Tests for both cookies as sanity check.
    }
    getConfig() {
        if (!Cookies.get('auth_token')) {
            return {};
        }
        return {
            headers: {
                Authorization: `Bearer ${Cookies.get('auth_token')}`,
            }
        };
    }
    deleteAccount(){
        return axios.delete('/users/user', this.getConfig())
        .then(response => {
            return response.data;
        })
        .catch(error => {
            throw error.response ? error.response.data : new Error('Error deleting account');
        });
    }
    async getUserRole(username) {
        try {
            const response = await axios.get(`/users/${username}`);
            console.log('Response data:', response); 
            const role = response.data.role;
            return role;
        } catch (error) {
            throw error.response ? error.response.data : new Error('Error getting user role');
        }
    }
}

export default new UserService()