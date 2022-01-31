import {MutationTree} from "vuex";
import {AuthState} from "@/stores/auth/types";
import {AuthUser} from "@/models/authUser";

export const mutations = <MutationTree<AuthState>>{
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