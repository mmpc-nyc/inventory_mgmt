import {ActionTree, Commit, MutationTree} from "vuex";
import {AuthUser} from "@/models/authUser";
import LocalStorageService from "@/services/LocalStorageService";
import {config} from "@/config/config";
import axiosInstance from "@/services/AxiosInstance";

const API_AUTH_URL = `${config.HOST}/auth/`;

class State {
    authUser: AuthUser = LocalStorageService.getUser()
}

const mutations = <MutationTree<State>>{
    loginSuccess(state, authUser) {
        console.log(authUser)
        state.authUser = authUser;
    },
    loginFailure(state) {
        state.authUser = new AuthUser()
    },
    logout(state) {
        state.authUser = new AuthUser()
    },
    refreshToken(state, accessToken) {
        state.authUser.loggedIn = true;
        state.authUser.access = accessToken
    },
}

const actions = <ActionTree<State, any>>{
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

const authStore = {
    namespaced: true,
    state: new State(),
    actions: actions,
    mutations: mutations,
};

export default authStore;
