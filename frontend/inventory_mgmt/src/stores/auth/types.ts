import {AuthUser} from "@/models/authUser";
import LocalStorageService from "@/storage/auth/LocalAuthStorage";

export class AuthState {
    authUser: AuthUser = LocalStorageService.getAuthUser()
}