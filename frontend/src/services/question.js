import axios from './baseAxiosClient';
import Cookies from 'js-cookie';

class QuestionService{
    async newQuestion(artistUsername, questionText){
        try {
            const response = await axios.post('/questions', {
                'artist_username': artistUsername,
                'question_text': questionText,
            }, this.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    // Returns the current user's top 3 non-archived questions by importance.
    async getTopQuestions() {
        try {
            const response = await axios.get('/questions/top', this.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }


    async getQuestions() {
        try {
            const response = await axios.get('/questions/', this.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async archiveQuestion(id) {
        try {
            const response = await axios.post('/questions/archive', null, {... (this.getConfig()), params: {question_id: id}});
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    getConfig() {
        return {
            headers: {
                Authorization: `Bearer ${Cookies.get('auth_token')}`,
            }
        };
    }
}

export default new QuestionService()