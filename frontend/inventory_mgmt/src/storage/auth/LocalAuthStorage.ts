import {AuthUser} from "@/models/authUser";
import {plainToClass} from "class-transformer";
import AuthStorage from "@/storage/auth/types";

class LocalAuthStorage implements AuthStorage{

  getAuthUser() :AuthUser {
    const data = localStorage.getItem("authUser")
    if (data){
      return plainToClass(AuthUser, JSON.parse(data))
    }
    return new AuthUser()
  }

  setAuthUser(authUser: AuthUser) {
    localStorage.setItem("authUser", JSON.stringify(authUser));
  }

  removeAuthUser() {
    localStorage.removeItem("authUser");
  }
}

export default new LocalAuthStorage();
