import axios from './baseAxiosClient';
import UserService from './user'

class PlaylistService {
    async createPlaylist(data) {
        try {
            const response = await axios.post('/playlist/', data, UserService.getConfig());
            return response.data;
        } catch (err) {
            throw err.response ? err.response.data.detail[0].msg : err.message; // Fallback to HTTP error message if no detail is provided.
        }
    }
    async update(id, data) {
        try {
            const response = await axios.put('/playlist/' + id, data, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async addSong(playlistID, song) {
        try {
            const response = await axios.post('/playlist/' + playlistID + '/song/' + song.song_id, {}, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async removeSong(playlistID, song) {
        try {
            const response = await axios.delete('/playlist/' + playlistID + '/song/' + song.song_id, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async reorderSongs(playlistID, songIDs) {
        try {
            const response = await axios.put('/playlist/' + playlistID + '/reorder', {song_ids: songIDs}, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async delete(id) {
        try {
            const response = await axios.delete('/playlist/' + id, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async get(id) {
        try {
            const response = await axios.get('/playlist/' + id, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async getUserPlaylists(username) {
        try {
            const response = await axios.get('/playlist/user/' + username, UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default new PlaylistService()