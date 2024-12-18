import axios from "./baseAxios.js";

export async function registerUser(username, email, password) {
    try {
      const response = await axios.post('/users/user', {
        username: username,
        email: email,
        password: password,
      });
      return response.data;
    } catch (error) {
      throw error; // Rethrow the error so it can be handled by the caller
    }
  }


export async function registerArtist(username, email, password) {
    try {
      const response = await axios.post('/users/user', {
        username: username,
        email: email,
        password: password,
        genre: "Rock",
        role: "artist",
      });
      return response.data;
    } catch (error) {
      throw error; // Rethrow the error so it can be handled by the caller
    }
  }