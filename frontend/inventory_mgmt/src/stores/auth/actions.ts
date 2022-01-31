import {ActionTree, Commit} from "vuex";
import {AuthState} from "@/stores/auth/types";
import axiosInstance from "@/services/AxiosInstance";
import {AuthUser} from "@/models/authUser";
import LocalStorageService from "@/services/LocalStorageService";
import {config} from "@/config/config";

const API_AUTH_URL = `${config.HOST}/auth/`;

export const actions = <ActionTree<AuthState, any>>{
    login({commit}: { commit: Commit }, userInput) {
        axiosInstance
            .post(`${API_AUTH_URL}jwt/create`, {
                username: userInput.username,
                password: userInput.password
            })
            .then((response) => {
                if (response.data.access) {
                    const authUser: AuthUser = new AuthUser()
                    authUser.username = userInput.username
                    authUser.loggedIn = true
                    authUser.access = response.data.access
                    authUser.refresh = response.data.refresh
                    LocalStorageService.setUser(authUser);
                    commit("loginSuccess", authUser)
                    return Promise.resolve(authUser);
                }
                commit("loginFailure");
                return Promise.reject('Invalid Credentials');
            }).catch(response => {
            console.log('Failed to Connect to Server')
        });
    },
    logout({commit}: { commit: Commit }) {

        LocalStorageService.removeUser();
        commit("logout");
    },
    refreshToken({commit}, accessToken) {
        commit("refreshToken", accessToken);
    },
}
