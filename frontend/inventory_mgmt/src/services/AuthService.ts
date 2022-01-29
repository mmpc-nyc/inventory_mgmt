import axiosInstance from "@/services/AxiosInstance";
import LocalStorageService from "./LocalStorageService";
import {AuthUser} from "@/models/authUser";
import {config} from "@/config/config";

const API_AUTH_URL = `${config.HOST}/auth/`; /* TODO Change this */

class AuthService {
  login(username: string, password: string) {
    return axiosInstance
      .post(API_AUTH_URL + "jwt/create", {
        username: username,
        password: password,
      })
      .then((response) => {
        if (response.data.access) {
          const authUser: AuthUser = new AuthUser(username, true, response.data.access, response.data.refresh )
          LocalStorageService.setUser(authUser);
          return authUser
        }
        return response
      });
  }

  logout() {
    LocalStorageService.removeUser();
  }
}

export default new AuthService();
