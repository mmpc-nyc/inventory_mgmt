import {anonUser, AuthUser} from "@/models/authUser";
import {plainToClassFromExist} from "class-transformer";

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
      return plainToClassFromExist(anonUser, JSON.parse(data)) || anonUser
    }
    return anonUser
  }

  setUser(authUser: AuthUser) {
    localStorage.setItem("authUser", JSON.stringify(authUser));
  }

  removeUser() {
    localStorage.removeItem("user");
  }
}

export default new LocalStorageService();
