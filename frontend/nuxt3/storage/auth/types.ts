import {AuthUser} from "~/models/authUser";

export interface AuthStorage {
    getAuthUser(): AuthUser
    setAuthUser(authUser: AuthUser): void
    removeAuthUser(authUser: AuthUser): void

}

export default AuthStorage