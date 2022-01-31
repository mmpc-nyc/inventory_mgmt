import {AuthUser} from "@/models/authUser";
import LocalStorageService from "@/services/LocalStorageService";

export class AuthState {
    authUser: AuthUser = LocalStorageService.getUser()
}