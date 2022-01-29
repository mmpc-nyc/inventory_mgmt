import {AuthUser} from "@/models/authUser";
import {plainToClass} from "class-transformer";

class LocalStorageService {
  getLocalRefreshToken() {
    return this.getUser().refresh
  }

  getLocalAccessToken() {
    return this.getUser().access;
  }

  updateLocalAccessToken(access: string) {
    const authUser = this.getUser()
    authUser.access = access;
    this.setUser(authUser)
  }

  getUser() :AuthUser {
    const data = localStorage.getItem("authUser")
    if (data){
      return plainToClass(AuthUser, JSON.parse(data))
    }
    return new AuthUser()
  }

  setUser(authUser: AuthUser) {
    localStorage.setItem("authUser", JSON.stringify(authUser));
  }

  removeUser() {
    localStorage.removeItem("authUser");
  }
}

export default new LocalStorageService();
