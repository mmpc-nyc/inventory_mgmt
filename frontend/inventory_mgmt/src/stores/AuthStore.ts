import AuthService from "@/services/AuthService";
import {ActionTree, Commit, MutationTree} from "vuex";
import {AuthUser, anonUser} from "@/models/authUser";
import LocalStorageService from "@/services/LocalStorageService";

class State {
    authUser: AuthUser = LocalStorageService.getUser()
}

const mutations = <MutationTree<State>>{
    loginSuccess(state, user) {
        state.authUser = user;
    },
    loginFailure(state) {
        state.authUser = anonUser
    },
    logout(state) {
        state.authUser = anonUser
    },
    refreshToken(state, accessToken) {
        state.authUser.loggedIn = true;
        state.authUser.access = accessToken
    },
}

const actions = <ActionTree<State, any>>{
    login({commit}: { commit: Commit }, userInput) {
        return AuthService.login(userInput.username, userInput.password).then(
            (user) => {
                commit("loginSuccess", user);
                return Promise.resolve(user);
            },
            (error) => {
                commit("loginFailure");
                return Promise.reject(error);
            }
        );
    },
    logout({commit}: { commit: Commit }) {
        AuthService.logout();
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
