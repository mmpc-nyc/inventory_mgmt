import {config} from "@/config/config";
import axios from "axios"
import LocalAuthStorage from "@/storage/auth/LocalAuthStorage";
import {AuthUser} from "@/models/authUser";


const authService = {
    BASE_URL: `${config.HOST}/auth/`,
    AuthStorage: LocalAuthStorage,

    getAccessToken(): string {
        return this.AuthStorage.getAuthUser().access
    },

    getRefreshToken(): string {
        return this.AuthStorage.getAuthUser().refresh
    },

    setAccessToken(access: string) {
        const authUser = this.AuthStorage.getAuthUser()
        authUser.access = access;
        this.AuthStorage.setAuthUser(authUser)
    },

    async login(username: string, password: string): Promise<AuthUser> {

        return axios.post(`${this.BASE_URL}jwt/create`, {username: username, password: password}).then(response => {
            const authUser: AuthUser = new AuthUser()
            if (response.data.access) {
                authUser.username = username
                authUser.loggedIn = true
                authUser.access = response.data.access
                authUser.refresh = response.data.refresh
                this.AuthStorage.setAuthUser(authUser)
                return Promise.resolve(authUser)
            }
            console.log(response, response.data.code)
            return Promise.reject(response)
        }).catch(error => {
            if (error.response) {
                console.log(error.response.data, error.response.status)
            } else if (error.request) {
                console.log(error.request)
            } else {
                console.log(error.message)
            }
            return Promise.reject(error)
        })
    },
    async logout() {
        //TODO Implement server logout
        this.AuthStorage.removeAuthUser()
    },

    async refresh(): Promise<string> {
        const response = await axios.post(`${config.HOST}/auth/jwt/refresh`, {refresh: this.getRefreshToken()})
        if (response.data.access) {
            this.setAccessToken(response.data.access)
            return Promise.resolve(response.data.access)
        }
        return Promise.reject(response)

    }
}

export default authService