import axiosInstance from "@/services/AxiosInstance";
import TokenService from "./TokenService";
import {User} from "@/models/user";

const API_AUTH_URL = "http://localhost:8000/auth/"; /* TODO Change this */

class AuthService {
  login(user: User) {
    return axiosInstance
      .post(API_AUTH_URL + "jwt/create", {
        username: user.username,
        password: user.password,
      })
      .then((response) => {
        if (response.data.access) {
          TokenService.setUser(response.data);
        }
        return response.data;
      });
  }

  logout() {
    TokenService.removeUser();
  }
}

export default new AuthService();
