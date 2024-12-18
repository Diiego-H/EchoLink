import axios from './baseAxiosClient';
import UserService from './user'

class QuestionService {
    // Retrieves the questions asked to the logged-in user (if they are an artist)
    // or asked by the user (if they are a listener)
    async getUserQuestions() {
        try {
            const response = await axios.get('/questions', UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async answerQuestion(answer, questionId){
        try {
            const response = await axios.post('/questions/answer',{
                'question_id': questionId,
                'response_text': answer,
            }, 
            UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
    async rejectQuestion(answer, questionId){
        try {
            const response = await axios.post('/questions/reject',{
                'question_id': questionId,
                'response_text': answer,
            }, 
            UserService.getConfig());
            return response.data;
        } catch (error) {
            throw error;
        }
    }
}

export default new QuestionService()