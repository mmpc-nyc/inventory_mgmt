import {ActionTree, Commit} from "vuex";
import {AuthState} from "~/stores/auth/types";
import authService from "~/services/AuthService";
import AuthService from "~/services/AuthService";

export const actions = <ActionTree<AuthState, any>>{
    login({commit}: { commit: Commit }, userInput) {
        return authService.login(userInput.username, userInput.password)
            .then(
                function resolve(authUser) {
                    commit("loginSuccess", authUser)
                },
                function reject(error) {
                    commit("loginFailure", error)
                }
            ).catch((error) => {
                    commit("loginFailure", error)
                }
            )
    },
    logout({commit}: { commit: Commit }) {

        AuthService.logout().finally(() => {
            commit("logout");
        });
    },
    setAccessToken({commit}, accessToken) {
        AuthService.setAccessToken(accessToken);
        commit("setAccessToken", accessToken);
    },
}
