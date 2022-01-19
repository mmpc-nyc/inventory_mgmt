import axios from 'axios'

const API_AUTH_URL = 'http://localhost:8000/auth/'  /* TODO Change this */

class AuthService {
    login(user) {
        return axios.post(
            API_AUTH_URL + "jwt/create",
            {
                username: user.username,
                password: user.password
            }
        ).then(response => {
            if (response.data.access_token) {
                localStorage.setItem('user', JSON.stringify(response.data));
            }
            return response.data;
        })
    }

    logout() {
        localStorage.removeItem('user')
    }
}

export default new AuthService()