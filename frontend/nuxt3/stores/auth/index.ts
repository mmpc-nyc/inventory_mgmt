import {AuthState} from "~/stores/auth/types";
import {mutations} from "~/stores/auth/mutations";
import {actions} from "~/stores/auth/actions";

const authStore = {
    namespaced: true,
    state: new AuthState(),
    actions: actions,
    mutations: mutations,
    getters: {
        // experimenting
        isLoggedIn: (state: AuthState) => {
            return state.authUser.loggedIn
        }
    }
};

export default authStore;
